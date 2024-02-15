import { prompt, getNewTestClient, sleep } from "./common.js"

const latencies = []

async function createBenchClient(joinCode, number) {
    const [client, email] = await getNewTestClient(number)

    client.on("connect", async () => {
        client.emit("session_connect", joinCode, (code, msg) => {
            console.log(email + " est connecté")
        })
    })

    client.on("next_question", async (data) => {
        // Type de question
        if (data.type.includes("open")) {
            const questionId = data.question.id

            await sleep(Math.random() * 1000)

            const start = Date.now()
            client.emit("user_open_answer", questionId, "SPQR", (code, msg) => { // XXX : une seule réponse pour l'instant
                const latency = (Date.now() - start) / 1000
                latencies.push(latency)
                console.log(email + " à répondu ouvertement (latence : " + latency + "s")
            })
        } else {
            // Question type QCM
            const nAnswers = data.answers.length
            const number = data.answers[Math.floor(Math.random() * nAnswers)].id

            await sleep(Math.random() * 1000)

            const start = Date.now()
            client.emit("user_answer", [number], (code, msg) => { // XXX : une seule réponse pour l'instant
                const latency = (Date.now() - start) / 1000
                latencies.push(latency)
                console.log(email + " à répondu (latence : " + latency + "s")
            })
        }
    })

    client.on("session_end", (resultId) => {
        console.log(email + " a fini la session")
    })

    client.on("disconnect", () => {
        console.log(email + " est déconnecté")
        client.disconnect()
    })
}

async function main() {
    const joinCode = await prompt("Code pour rejoindre la session : ")

    for (let index = 0; index < 300; index++) {
        createBenchClient(joinCode, index)
    }
}

process.stdin.on("keypress", (str, key) => {
    if (key.ctrl && key.name === "r") {
        console.log("Moyenne des latences : " + latencies.reduce((a, b) => a + b, 0) / latencies.length)
    }
})

main()
