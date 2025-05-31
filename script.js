class HangmanGame {
    constructor() {
        this.PHRASES = [
            'rocket launch',
            'cosmic voyage',
            'space station',
            'alien planet',
            'stellar wind',
            'galaxy quest',
            'moon landing',
            'solar system',
            'asteroid belt'
        ];

        this.timer = null;
        this.secondsLeft = 300;
        this.score = 0;
        this.selectedPhrase = '';
        this.guessedPhrase = [];
        this.incorrectGuesses = 0;
        this.canvas = document.getElementById('hangman-canvas');
        this.ctx = this.canvas.getContext('2d');
        
        this.initGame();
        this.preventZoom();
    }

    preventZoom() {
        document.addEventListener('touchmove', (e) => {
            if (e.scale !== 1) { e.preventDefault(); }
        }, { passive: false });

        document.addEventListener('gesturestart', (e) => {
            e.preventDefault();
        });

        document.addEventListener('gesturechange', (e) => {
            e.preventDefault();
        });

        document.addEventListener('gestureend', (e) => {
            e.preventDefault();
        });
    }

    initGame() {
        this.selectRandomPhrase();
        this.createLetterButtons();
        this.drawGallows();
        this.startTimer();
        this.updatePhraseDisplay();
    }

    selectRandomPhrase() {
        this.selectedPhrase = this.PHRASES[Math.floor(Math.random() * this.PHRASES.length)].toLowerCase();
        this.guessedPhrase = this.selectedPhrase.split('').map(char => 
            char === ' ' ? ' ' : '_'
        );
    }

    createLetterButtons() {
        const container = document.getElementById('letter-buttons');
        container.innerHTML = '';
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('').forEach(letter => {
            const button = document.createElement('button');
            button.textContent = letter;
            button.addEventListener('click', () => this.handleGuess(letter.toLowerCase(), button));
            button.addEventListener('touchstart', (e) => {
                e.preventDefault();
                this.handleGuess(letter.toLowerCase(), button);
            });
            container.appendChild(button);
        });
    }

    handleGuess(letter, button) {
        if (button.disabled) return;
        
        button.disabled = true;
        
        if (this.selectedPhrase.includes(letter)) {
            this.guessedPhrase = this.guessedPhrase.map((char, index) => 
                this.selectedPhrase[index] === letter ? letter : char
            );
            this.score += 1;
        } else {
            this.incorrectGuesses++;
            this.drawHangman();
            this.score -= 0.5;
        }

        this.updatePhraseDisplay();
        this.updateScoreDisplay();
        this.checkGameStatus();
    }

    drawGallows() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.strokeStyle = 'white';
        this.ctx.lineWidth = 4;
        this.ctx.beginPath();
        this.ctx.moveTo(50, 180);
        this.ctx.lineTo(150, 180);
        this.ctx.lineTo(100, 50);
        this.ctx.lineTo(100, 70);
        this.ctx.stroke();
    }

    drawHangman() {
        const parts = [
            () => {
                this.ctx.beginPath();
                this.ctx.arc(100, 90, 20, 0, Math.PI * 2);
                this.ctx.stroke();
            },
            () => {
                this.ctx.beginPath();
                this.ctx.moveTo(100, 110);
                this.ctx.lineTo(100, 150);
                this.ctx.stroke();
            },
            () => {
                this.ctx.beginPath();
                this.ctx.moveTo(100, 120);
                this.ctx.lineTo(70, 140);
                this.ctx.stroke();
            },
            () => {
                this.ctx.beginPath();
                this.ctx.moveTo(100, 120);
                this.ctx.lineTo(130, 140);
                this.ctx.stroke();
            },
            () => {
                this.ctx.beginPath();
                this.ctx.moveTo(100, 150);
                this.ctx.lineTo(70, 180);
                this.ctx.stroke();
            },
            () => {
                this.ctx.beginPath();
                this.ctx.moveTo(100, 150);
                this.ctx.lineTo(130, 180);
                this.ctx.stroke();
            }
        ];

        if (this.incorrectGuesses <= parts.length) {
            parts[this.incorrectGuesses - 1]();
        }
    }

    updatePhraseDisplay() {
        document.getElementById('phrase-display').textContent = 
            this.guessedPhrase.map(char => char.toUpperCase()).join(' ');
    }

    updateScoreDisplay() {
        document.getElementById('score').textContent = this.score.toFixed(2);
    }

    startTimer() {
        this.timer = setInterval(() => {
            this.secondsLeft--;
            const minutes = Math.floor(this.secondsLeft / 60);
            const seconds = this.secondsLeft % 60;
            document.getElementById('timer').textContent = 
                `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
            
            this.score -= 0.01;
            this.updateScoreDisplay();

            if (this.secondsLeft <= 0) {
                this.gameOver('Time is up!');
            }
        }, 1000);
    }

    checkGameStatus() {
        if (!this.guessedPhrase.includes('_')) {
            this.gameWon();
        } else if (this.incorrectGuesses >= 6) {
            this.gameOver('Game Over!');
        }
    }

    gameWon() {
        clearInterval(this.timer);
        this.showMessage('Congratulations! You won!');
        setTimeout(() => this.resetGame(), 2000);
    }

    gameOver(message) {
        clearInterval(this.timer);
        this.showMessage(`${message} Phrase: ${this.selectedPhrase.toUpperCase()}`);
        setTimeout(() => this.resetGame(), 2000);
    }

    showMessage(message) {
        const messageEl = document.getElementById('game-message');
        messageEl.textContent = message;
        setTimeout(() => {
            messageEl.textContent = '';
        }, 2000);
    }

    resetGame() {
        this.secondsLeft = 300;
        this.score = 0;
        this.incorrectGuesses = 0;
        this.drawGallows();
        this.selectRandomPhrase();
        this.createLetterButtons();
        this.updatePhraseDisplay();
        this.updateScoreDisplay();
        this.startTimer();
    }
}

new HangmanGame();