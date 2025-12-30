const grid = document.getElementById('grid');
const status = document.getElementById('status');
let cells = [];

// API endpoint - change this if deploying to different URL
const API_URL = window.location.origin;

function initGrid() {
    grid.innerHTML = '';
    cells = [];
    for (let i = 0; i < 81; i++) {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'cell';
        input.maxLength = 1;
        input.addEventListener('input', handleInput);
        input.addEventListener('keydown', handleKeydown);
        grid.appendChild(input);
        cells.push(input);
    }
}

function handleInput(e) {
    const value = e.target.value;
    if (value && (value < '1' || value > '9')) {
        e.target.value = '';
    }
    e.target.classList.remove('solved');
}

function handleKeydown(e) {
    const index = cells.indexOf(e.target);
    let nextIndex = -1;
    switch(e.key) {
        case 'ArrowUp': nextIndex = index - 9; e.preventDefault(); break;
        case 'ArrowDown': nextIndex = index + 9; e.preventDefault(); break;
        case 'ArrowLeft': nextIndex = index - 1; e.preventDefault(); break;
        case 'ArrowRight': nextIndex = index + 1; e.preventDefault(); break;
    }
    if (nextIndex >= 0 && nextIndex < 81) {
        cells[nextIndex].focus();
    }
}

function getBoardFromGrid() {
    const board = [];
    for (let i = 0; i < 9; i++) {
        const row = [];
        for (let j = 0; j < 9; j++) {
            const value = cells[i * 9 + j].value;
            row.push(value ? parseInt(value) : 0);
        }
        board.push(row);
    }
    return board;
}

function setBoardToGrid(board, markSolved = false) {
    for (let i = 0; i < 9; i++) {
        for (let j = 0; j < 9; j++) {
            const cell = cells[i * 9 + j];
            const value = board[i][j];
            if (value !== 0) {
                cell.value = value;
                if (markSolved) {
                    cell.classList.add('solved');
                }
            }
        }
    }
}

function showStatus(message, type) {
    status.textContent = message;
    status.className = 'status ' + type;
}

function hideStatus() {
    status.className = 'status';
}

async function solvePuzzle() {
    const board = getBoardFromGrid();
    const originalBoard = board.map(row => [...row]);
    showStatus('Solving puzzle...', 'loading');
    
    try {
        const response = await fetch(`${API_URL}/solve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ board: board })
        });
        
        const data = await response.json();
        
        if (data.success) {
            for (let i = 0; i < 9; i++) {
                for (let j = 0; j < 9; j++) {
                    if (originalBoard[i][j] === 0 && data.solution[i][j] !== 0) {
                        cells[i * 9 + j].classList.add('solved');
                    }
                }
            }
            setBoardToGrid(data.solution, true);
            showStatus('✓ Puzzle solved successfully!', 'success');
        } else {
            showStatus('✗ ' + data.message, 'error');
        }
    } catch (error) {
        showStatus('✗ Error: Could not solve puzzle', 'error');
        console.error(error);
    }
}

function clearGrid() {
    cells.forEach(cell => {
        cell.value = '';
        cell.classList.remove('solved');
    });
    hideStatus();
}

function loadExample() {
    const example = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ];
    clearGrid();
    setBoardToGrid(example);
    hideStatus();
}

// Initialize grid on page load
initGrid();