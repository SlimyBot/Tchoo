import { prompt, getClient, waitUntilInput, createSession } from "./common.js"

async function main() {
    const client = await getClient(process.env.OWNER_EMAIL, process.env.PASSWORD)

    client.on("connect", async () => {
        console.log("Connecté")

        console.log("Création d'une nouvelle session...");
        const joinCode = await createSession(1, client.auth)
        console.log("OK : " + joinCode);

        client.emit("session_connect", joinCode, async (code, msg) => {
            console.log(code + " : " + msg)

            // lancement de la session quand c'est envoyé
            await waitUntilInput("start", "Ecrire 'start' pour démarrer : ")
            client.emit("initiate_next_question", (code, msg) => {
                console.log(code + " : " + msg)
            })
        })
    })

    client.on("next_question", async (data) => {
        console.log("Question : " + data.question.text)

        await waitUntilInput("next", "Ecrire next pour passer à la prochaine question : ")
        client.emit("initiate_next_question", async (code, msg) => {
            console.log(code + " : " + msg)

            if (msg === "Fin du questionaire") {
                await waitUntilInput("end", "Ecrire 'end' pour terminer la session : ")
                client.emit("end_session", (code, msg) => {
                    console.log(code + " : " + msg)
                    client.disconnect()
                })
            }
        })
    })

    client.on("user_answered", (email) => {
        console.log(email + " à répondu")
    })

    client.on("user_join", (email) => {
        console.log(email + " à rejoind")
    })

    client.on("user_leave", (email) => {
        console.log(email + " à quitté")
    })

    client.on("disconnect", () => {
        console.log("Déconecté de la session")
    })
}

main()
