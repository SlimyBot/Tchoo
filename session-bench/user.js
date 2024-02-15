import { prompt, getClient } from "./common.js"

async function main() {
    const client = await getClient(process.env.EMAIL, process.env.PASSWORD)

    client.on("connect", async () => {
        console.log("Connecté")

        const joinCode = await prompt("Code pour rejoindre la session : ")

        client.emit("session_connect", joinCode, (code, msg) => {
            console.log(code + " : " + msg)
        })
    })

    client.on("next_question", async (data) => {
        console.log(data)

        let number = parseInt(await prompt("Numéro de la question : "))

        client.emit("user_answer", [number], (code, msg) => { // XXX : une seule réponse pour l'instant
            console.log(code + " : " + msg)
        })
    })

    client.on("session_end", (resultId) => {
        console.log("Notification de fin de session avec comme id de resultats : " + resultId)
    })

    client.on("disconnect", () => {
        console.log("Déconnecté de la session")
        client.disconnect()
        process.exit()
    })
}

main()
