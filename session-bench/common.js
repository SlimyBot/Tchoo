import "dotenv/config"
import { io } from "socket.io-client"
import * as readline from "readline"
import fetch from "node-fetch"
import https from "https"

const HOST_BASE = "10.22.27.3"
const HTTP_URL = `https://${HOST_BASE}`
const WS_URL = `wss://${HOST_BASE}`

const httpsAgent = new https.Agent({
    rejectUnauthorized: false,
})

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
})
export const prompt = (query) =>
    new Promise((resolve) => rl.question(query, resolve))

export function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms))
}

export async function createSession(surveyId, jwt) {
    let res = await fetch(`${HTTP_URL}/api/sessions/create`, {
        method: "POST",
        headers: {
            Authorization: `Bearer ${jwt}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            survey_id: surveyId,
            is_public: true,
        }),
    })

    let json = await res.json()

    return json.join_code
}

async function fetchJWT(email, password) {
    let data = new URLSearchParams()
    data.append("username", email)
    data.append("password", password)

    let res = await fetch(`${HTTP_URL}/api/users/login`, {
        method: "POST",
        contentType: "application/x-www-form-urlencoded",
        body: data,
    })

    let json = await res.json()

    if (res.status === 200) {
        return json.access_token
    }

    return null
}

export async function getClient(email, password) {
    console.log("Authentification de " + email + "...")
    const token = await fetchJWT(email, password)
    console.log("OK")
    console.log()

    return io(`${WS_URL}/session`, {
        path: "/ws",
        auth: token,
    })
}

export async function getGuestClient(number) {
    await sleep(Math.random() * 8000)

    let token = await fetchJWT(`guest-${number}@guest.com`, "pw" + number)

    if (token === null) {
        await fetch(`${HTTP_URL}/api/users/register`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: `guest-${number}@guest.com`,
                password: "pw" + number,
            }),
        })

        token = await fetchJWT(`guest-${number}@guest.com`, "pw" + number)
    }

    return [
        io(`${WS_URL}/session`, {
            path: "/ws",
            auth: token,
        }),
        `guest-${number}@guest.com`,
    ]
}

export async function getNewTestClient(number) {
    await sleep(number * 250)
    const res = await fetch(
        `${HTTP_URL}/api/users/dev_only_get_jwt/tester-${number}@mail.com`,
        {
            agent: httpsAgent,
        }
    )

    const token = await res.json()

    return [
        io(`${WS_URL}/session`, {
            path: "/ws",
            auth: token,
            rejectUnauthorized: false,
            transports: ["websocket"]
        }),
        `tester-${number}@mail.com`,
    ]
}

export async function waitUntilInput(match, promptText) {
    let res = ""
    while (res !== match) {
        res = await prompt(promptText)
    }
}
