document.addEventListener('DOMContentLoaded', function() {
    console.log('Script loaded - Starting debug...');

    // Get elements
    const inputText = document.getElementById('inputText');
    const outputText = document.getElementById('outputText');
    const convertBtn = document.getElementById('convertBtn');
    const clearBtn = document.getElementById('clearBtn');
    const copyBtn = document.getElementById('copyBtn');
    const textToNumBtn = document.getElementById('textToNum');
    const numToTextBtn = document.getElementById('numToText');
    const separatorSelect = document.getElementById('separator');

    // Current state
    let currentDirection = 'text_to_num';
    let currentSeparator = '/';

    // Setup event listeners
    textToNumBtn.addEventListener('click', () => {
        currentDirection = 'text_to_num';
        textToNumBtn.classList.add('active');
        numToTextBtn.classList.remove('active');
        inputText.placeholder = 'Enter text (e.g., HELLO)...';
    });

    numToTextBtn.addEventListener('click', () => {
        currentDirection = 'num_to_text';
        numToTextBtn.classList.add('active');
        textToNumBtn.classList.remove('active');
        inputText.placeholder = 'Enter numbers (e.g., 8/5/12/12/15)...';
    });

    separatorSelect.addEventListener('change', (e) => {
        currentSeparator = e.target.value;
    });

    clearBtn.addEventListener('click', () => {
        inputText.value = '';
        outputText.textContent = 'Result will appear here...';
    });

    // FIXED CONVERT FUNCTION
    convertBtn.addEventListener('click', async function() {
        const text = inputText.value.trim();

        if (!text) {
            alert('Please enter some text');
            return;
        }

        console.log('Sending request:', {
            text: text,
            direction: currentDirection,
            separator: currentSeparator
        });

        try {
            // Show loading
            convertBtn.disabled = true;
            convertBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Converting...';

            // Send request
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    direction: currentDirection,
                    separator: currentSeparator
                })
            });

            console.log('Response status:', response.status);

            // Check if response is OK
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Get response text first for debugging
            const responseText = await response.text();
            console.log('Raw response:', responseText);

            // Try to parse as JSON
            let data;
            try {
                data = JSON.parse(responseText);
            } catch (jsonError) {
                console.error('JSON parse error:', jsonError);
                throw new Error('Invalid JSON response from server');
            }

            console.log('Parsed response:', data);

            if (data.success) {
                outputText.textContent = data.result;
                // Show success message
                showMessage('Conversion successful!', 'success');
            } else {
                throw new Error(data.error || 'Conversion failed');
            }

        } catch (error) {
            console.error('Error:', error);
            outputText.textContent = `Error: ${error.message}`;
            showMessage(`Error: ${error.message}`, 'error');
        } finally {
            // Reset button
            convertBtn.disabled = false;
            convertBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Convert Now';
        }
    });

    // Copy function
    copyBtn.addEventListener('click', function() {
        const text = outputText.textContent;
        if (text && text !== 'Result will appear here...' && !text.startsWith('Error')) {
            navigator.clipboard.writeText(text).then(() => {
                showMessage('Copied to clipboard!', 'success');
            });
        }
    });

    // Simple message function
    function showMessage(message, type) {
        // Create message element
        const msg = document.createElement('div');
        msg.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            z-index: 9999;
            animation: fadeIn 0.3s;
            ${type === 'success' ? 'background: #4CAF50;' : 'background: #f44336;'}
        `;
        msg.textContent = message;
        document.body.appendChild(msg);

        // Remove after 3 seconds
        setTimeout(() => {
            msg.style.animation = 'fadeOut 0.3s';
            setTimeout(() => msg.remove(), 300);
        }, 3000);
    }

    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeOut {
            from { opacity: 1; transform: translateY(0); }
            to { opacity: 0; transform: translateY(-20px); }
        }
        .dir-btn.active {
            background: #667eea !important;
            color: white !important;
        }
    `;
    document.head.appendChild(style);

    // Test connection on load
    console.log('Testing connection...');
    fetch('/direct-test')
        .then(r => r.text())
        .then(t => console.log('Connection test:', t.substring(0, 50)))
        .catch(e => console.error('Connection failed:', e));
});
