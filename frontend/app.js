async function executeCommand() {

    const routerIp =
        document.getElementById("routerIp").value.trim();

    const command =
        document.getElementById("routerCommand").value.trim();

    const output =
        document.getElementById("output");

    const status =
        document.getElementById("status");

    const button =
        document.getElementById("executeButton");


    if (!routerIp) {

        status.textContent =
            "Please enter Router IP address";

        return;
    }


    if (!command) {

        status.textContent =
            "Please enter Router command";

        return;
    }


    button.disabled = true;

    button.textContent = "Connecting...";

    status.textContent =
        "Connecting to router...";

    output.textContent = "";


    try {

        const response = await fetch(
            "/api/execute",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    ip: routerIp,
                    command: command
                })
            }
        );


        const data = await response.json();


        if (data.success) {

            status.textContent =
                "Command executed successfully";

            output.textContent =
                data.output;

        } else {

            status.textContent =
                "Error: " + data.message;

            output.textContent =
                data.message;
        }


    } catch (error) {

        status.textContent =
            "Cannot connect to backend";

        output.textContent =
            error.toString();

    } finally {

        button.disabled = false;

        button.textContent =
            "Execute Command";
    }
}
