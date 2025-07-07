function sendMessage() {
    let userInputField = document.getElementById("user-input");
    let userInput = userInputField.value.trim();
    if (!userInput) return;

    let chatBox = document.getElementById("chat-box");
    let userMessage = document.createElement("div");
    userMessage.classList.add("message", "user-message");
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);
    userInputField.value = ""; 
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch("/dashboard", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({ "user-input": userInput })
    })
    .then(response => response.text())
    .then(data => {
        let botMessage = document.createElement("div");
        botMessage.classList.add("message", "chatbot-message");
        botMessage.innerHTML = data;
        chatBox.appendChild(botMessage);
        chatBox.scrollTop = chatBox.scrollHeight; 
    })
    .catch(error => console.error("Error:", error));
}
