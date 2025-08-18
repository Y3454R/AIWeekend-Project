HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vug Assistant</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        #chat-container {
            width: 100%;
            max-width: 700px;
            height: 90vh;
            max-height: 800px;
            background-color: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        #chat-header {
            padding: 16px;
            background-color: #4A90E2;
            color: white;
            font-weight: bold;
            text-align: center;
            border-bottom: 1px solid #ddd;
            flex-shrink: 0;
        }
        #chat-box {
            flex-grow: 1;
            padding: 20px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        .message {
            padding: 10px 15px;
            border-radius: 18px;
            max-width: 80%;
            line-height: 1.5;
        }
        .user-message {
            background-color: #4A90E2;
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 4px;
        }
        .bot-message {
            background-color: #e9ebee;
            color: #333;
            align-self: flex-start;
            border-bottom-left-radius: 4px;
        }
        .bot-message.thinking {
            color: #888;
            font-style: italic;
        }
        #input-area {
            display: flex;
            padding: 15px;
            border-top: 1px solid #ddd;
            flex-shrink: 0;
        }
        #user-input {
            flex-grow: 1;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 20px;
            margin-right: 10px;
            font-size: 16px;
        }
        #send-button {
            padding: 10px 20px;
            border: none;
            background-color: #4A90E2;
            color: white;
            border-radius: 20px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
        }
        #send-button:hover {
            background-color: #357ABD;
        }
    </style>
</head>
<body>
    <div id="chat-container">
        <div id="chat-header">Geotechnical Vug Assistant</div>
        <div id="chat-box">
             <div class="message bot-message">
                Hello! I can answer questions about the provided vug data from the Oman Basin. How can I help you? Try asking 'How many vugs are there?' or 'What is the largest vug detected?'.
            </div>
        </div>
        <form id="input-area" onsubmit="sendMessage(event)">
            <input type="text" id="user-input" placeholder="Ask a question..." autocomplete="off">
            <button id="send-button" type="submit">Send</button>
        </form>
    </div>

    <script>
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        const sendButton = document.getElementById('send-button');
        let chatHistory = [];

        function addMessage(sender, text) {
            const messageDiv = document.createElement('div');
            messageDiv.classList.add('message');
            if (sender === 'user') {
                messageDiv.classList.add('user-message');
            } else {
                messageDiv.classList.add('bot-message');
            }
            messageDiv.textContent = text;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
            return messageDiv;
        }

        async function sendMessage(event) {
            event.preventDefault();
            const question = userInput.value.trim();
            if (!question) return;

            addMessage('user', question);
            userInput.value = '';
            sendButton.disabled = true;

            const thinkingMessage = addMessage('bot', 'Thinking...');
            thinkingMessage.classList.add('thinking');

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        question: question,
                        history: chatHistory
                    }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();

                thinkingMessage.textContent = data.answer;
                thinkingMessage.classList.remove('thinking');

            } catch (error) {
                thinkingMessage.textContent = 'Sorry, something went wrong. Please try again.';
                thinkingMessage.classList.remove('thinking');
                console.error('Error:', error);
            } finally {
                sendButton.disabled = false;
                userInput.focus();
            }
        }
    </script>
</body>
</html>
"""
