document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatWindow = document.getElementById('chat-window');
    const sendButton = chatForm.querySelector('button[type="submit"]');

    // Display the initial greeting from the bot
    appendMessage("Hello! I am an advanced RAG chatbot. How can I assist you today?", 'bot');

    chatForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const userMessage = messageInput.value.trim();
        if (!userMessage) return;

        appendMessage(userMessage, 'user');
        messageInput.value = '';
        sendButton.disabled = true;

        const typingIndicator = appendMessage('...', 'bot');

        try {
            const response = await fetch('/get_answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: userMessage }),
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            
            // Update the typing indicator bubble with the real answer
            updateLastBotMessage(data.answer);

        } catch (error) {
            console.error('Error:', error);
            updateLastBotMessage('Sorry, something went wrong. Please check the terminal for errors.');
        } finally {
            sendButton.disabled = false;
            messageInput.focus(); // Keep focus on the input field
        }
    });

    function appendMessage(message, sender) {
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('flex', 'w-full', 'space-x-3', 'max-w-md', 'fade-in');

        const messageBubble = document.createElement('div');
        messageBubble.classList.add('p-3', 'rounded-xl');
        messageBubble.textContent = message;

        const timestamp = document.createElement('div');
        timestamp.classList.add('text-xs', 'text-gray-500', 'mt-1');
        timestamp.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        if (sender === 'user') {
            messageContainer.classList.add('ml-auto', 'justify-end');
            messageBubble.classList.add('bg-gradient-to-br', 'from-blue-500', 'to-blue-700', 'text-white');
            timestamp.classList.add('text-right');
            
            const messageContent = document.createElement('div');
            messageContent.appendChild(messageBubble);
            messageContent.appendChild(timestamp);
            messageContainer.appendChild(messageContent);
        } else { // Bot
            messageContainer.classList.add('mr-auto', 'justify-start');
            messageBubble.classList.add('bg-gray-700', 'text-white');
            timestamp.classList.add('text-left');

            const avatar = createAvatar();
            messageContainer.appendChild(avatar);

            const messageContent = document.createElement('div');
            messageContent.appendChild(messageBubble);
            messageContent.appendChild(timestamp);
            messageContainer.appendChild(messageContent);
        }
        
        chatWindow.appendChild(messageContainer);
        chatWindow.scrollTop = chatWindow.scrollHeight;
        return messageContainer;
    }

    function updateLastBotMessage(newMessage) {
        const allMessages = chatWindow.querySelectorAll('.flex.mr-auto');
        const lastBotMessageContainer = allMessages[allMessages.length - 1];
        if (lastBotMessageContainer) {
            const messageBubble = lastBotMessageContainer.querySelector('.p-3');
            messageBubble.textContent = newMessage;
            // Update timestamp
            const timestamp = lastBotMessageContainer.querySelector('.text-xs');
            timestamp.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        }
    }

    function createAvatar() {
        const avatarContainer = document.createElement('div');
        avatarContainer.classList.add('w-10', 'h-10', 'rounded-full', 'bg-gradient-to-br', 'from-indigo-500', 'to-purple-600', 'flex', 'items-center', 'justify-center', 'flex-shrink-0');
        const botIconSVG = `
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.546-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        `;
        avatarContainer.innerHTML = botIconSVG;
        return avatarContainer;
    }
});