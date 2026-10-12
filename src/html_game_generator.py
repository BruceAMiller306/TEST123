from __future__ import annotations


def generate_html_game() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Snake Arena (4" x 4")</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      background-color: #121216;
      color: #e0e0e0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 16px;
    }
    h1 {
      font-size: 1.25rem;
      margin-bottom: 8px;
      color: #ffffff;
      text-shadow: 0 0 10px rgba(0,255,0,0.4);
    }
    .hud {
      display: flex;
      gap: 16px;
      margin-bottom: 12px;
      font-size: 0.85rem;
      font-weight: 600;
    }
    .badge {
      padding: 4px 10px;
      border-radius: 4px;
      background: #1a1a24;
      border: 1px solid #333344;
    }
    .badge.green { color: #00ff00; border-color: #00aa00; }
    .badge.red { color: #ff4444; border-color: #aa2222; }
    .badge.orange { color: #ff9900; border-color: #aa6600; }

    /* The exact 4" by 4" black arena container */
    #arena-container {
      width: 4in;
      height: 4in;
      background-color: #000000;
      border: 2px solid #333333;
      box-shadow: 0 0 24px rgba(0, 0, 0, 0.8), 0 0 8px rgba(0, 255, 0, 0.2);
      position: relative;
      overflow: hidden;
    }
    canvas {
      display: block;
      width: 100%;
      height: 100%;
      background-color: #000000;
    }
    .overlay {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.82);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: #ffffff;
      font-weight: bold;
      text-align: center;
      padding: 16px;
    }
    .hidden {
      display: none !important;
    }
    .instructions {
      margin-top: 12px;
      font-size: 0.75rem;
      color: #888899;
      text-align: center;
      max-width: 4in;
      line-height: 1.4;
    }
    button.btn {
      margin-top: 10px;
      padding: 6px 14px;
      background: #00ff00;
      color: #000;
      border: none;
      border-radius: 4px;
      font-weight: bold;
      cursor: pointer;
    }
    button.btn:hover {
      background: #33ff33;
    }
  </style>
</head>
<body>

  <h1>Snake Arena</h1>

  <div class="hud">
    <div class="badge green">Green (You): <span id="len-green">5</span></div>
    <div class="badge red">Red (NPC): <span id="len-red">5</span></div>
    <div class="badge orange">Orange (NPC): <span id="len-orange">5</span></div>
  </div>

  <div id="arena-container">
    <canvas id="gameCanvas" width="384" height="384"></canvas>
    <div id="overlay" class="overlay hidden">
      <div id="overlay-msg" style="font-size: 1.1rem; margin-bottom: 8px;">GAME OVER</div>
      <button class="btn" onclick="resetGame()">Play Again</button>
    </div>
  </div>

  <div class="instructions">
    <strong>Rules:</strong> Steer with <strong>Arrow Keys</strong> or <strong>WASD</strong>. 2 Red & Orange NPCs attack you.<br>
    Running through a dot makes the snake of that color <strong>lose 1 square</strong>!
  </div>

  <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const GRID_SIZE = 24; // 24x24 grid on 384x384 canvas
    const CELL_PX = 384 / GRID_SIZE; // 16px per cell

    let greenSnake = [];
    let redSnake = [];
    let orangeSnake = [];
    let dots = []; // {x, y, color}

    let greenDir = {x: 1, y: 0};
    let nextGreenDir = {x: 1, y: 0};
    let redDir = {x: 0, y: 1};
    let orangeDir = {x: 0, y: -1};

    let isGameOver = false;
    let gameLoopInterval = null;

    function initGame() {
      // All snakes start with 5 squares
      greenSnake = [
        {x: 6, y: 12}, {x: 5, y: 12}, {x: 4, y: 12}, {x: 3, y: 12}, {x: 2, y: 12}
      ];
      redSnake = [
        {x: 18, y: 5}, {x: 18, y: 4}, {x: 18, y: 3}, {x: 18, y: 2}, {x: 18, y: 1}
      ];
      orangeSnake = [
        {x: 18, y: 19}, {x: 18, y: 20}, {x: 18, y: 21}, {x: 18, y: 22}, {x: 18, y: 23}
      ];

      greenDir = {x: 1, y: 0};
      nextGreenDir = {x: 1, y: 0};
      redDir = {x: 0, y: 1};
      orangeDir = {x: 0, y: -1};

      dots = [];
      spawnDot('green');
      spawnDot('red');
      spawnDot('orange');

      isGameOver = false;
      document.getElementById('overlay').classList.add('hidden');
      updateHUD();
    }

    function spawnDot(color) {
      const occupied = new Set();
      [...greenSnake, ...redSnake, ...orangeSnake].forEach(s => occupied.add(`${s.x},${s.y}`));
      dots.forEach(d => occupied.add(`${d.x},${d.y}`));

      const emptyCells = [];
      for (let x = 0; x < GRID_SIZE; x++) {
        for (let y = 0; y < GRID_SIZE; y++) {
          if (!occupied.has(`${x},${y}`)) emptyCells.push({x, y});
        }
      }
      if (emptyCells.length > 0) {
        const pick = emptyCells[Math.floor(Math.random() * emptyCells.length)];
        dots.push({x: pick.x, y: pick.y, color: color});
      }
    }

    function updateHUD() {
      document.getElementById('len-green').innerText = greenSnake.length > 0 ? greenSnake.length : 'DEAD';
      document.getElementById('len-red').innerText = redSnake.length > 0 ? redSnake.length : 'DEAD';
      document.getElementById('len-orange').innerText = orangeSnake.length > 0 ? orangeSnake.length : 'DEAD';
    }

    // NPC AI attacks green snake head
    function getAttackDirection(npcHead, currentDir, targetHead) {
      const candidates = [
        {x: 0, y: -1}, // UP
        {x: 0, y: 1},  // DOWN
        {x: -1, y: 0}, // LEFT
        {x: 1, y: 0}   // RIGHT
      ].filter(d => !(d.x === -currentDir.x && d.y === -currentDir.y));

      candidates.sort((a, b) => {
        const nextA = {x: (npcHead.x + a.x + GRID_SIZE) % GRID_SIZE, y: (npcHead.y + a.y + GRID_SIZE) % GRID_SIZE};
        const nextB = {x: (npcHead.x + b.x + GRID_SIZE) % GRID_SIZE, y: (npcHead.y + b.y + GRID_SIZE) % GRID_SIZE};
        const distA = Math.abs(nextA.x - targetHead.x) + Math.abs(nextA.y - targetHead.y);
        const distB = Math.abs(nextB.x - targetHead.x) + Math.abs(nextB.y - targetHead.y);
        return distA - distB;
      });

      return candidates[0] || currentDir;
    }

    function step() {
      if (isGameOver) return;

      // 1. NPC direction decisions attacking green snake
      if (greenSnake.length > 0) {
        const target = greenSnake[0];
        if (redSnake.length > 0) redDir = getAttackDirection(redSnake[0], redDir, target);
        if (orangeSnake.length > 0) orangeDir = getAttackDirection(orangeSnake[0], orangeDir, target);
      }

      // 2. Advance snakes
      greenDir = nextGreenDir;
      if (greenSnake.length > 0) {
        const head = greenSnake[0];
        const newHead = {
          x: (head.x + greenDir.x + GRID_SIZE) % GRID_SIZE,
          y: (head.y + greenDir.y + GRID_SIZE) % GRID_SIZE
        };
        greenSnake.unshift(newHead);
        greenSnake.pop();
      }

      if (redSnake.length > 0) {
        const head = redSnake[0];
        const newHead = {
          x: (head.x + redDir.x + GRID_SIZE) % GRID_SIZE,
          y: (head.y + redDir.y + GRID_SIZE) % GRID_SIZE
        };
        redSnake.unshift(newHead);
        redSnake.pop();
      }

      if (orangeSnake.length > 0) {
        const head = orangeSnake[0];
        const newHead = {
          x: (head.x + orangeDir.x + GRID_SIZE) % GRID_SIZE,
          y: (head.y + orangeDir.y + GRID_SIZE) % GRID_SIZE
        };
        orangeSnake.unshift(newHead);
        orangeSnake.pop();
      }

      // 3. Dot collisions: snake passing through dot makes snake of that color lose a square
      const allHeads = [];
      if (greenSnake.length > 0) allHeads.push({head: greenSnake[0], snake: 'green'});
      if (redSnake.length > 0) allHeads.push({head: redSnake[0], snake: 'red'});
      if (orangeSnake.length > 0) allHeads.push({head: orangeSnake[0], snake: 'orange'});

      const remainingDots = [];
      for (const dot of dots) {
        let eaten = false;
        for (const h of allHeads) {
          if (h.head.x === dot.x && h.head.y === dot.y) {
            eaten = true;
            // The snake with that color loses a square!
            if (dot.color === 'green' && greenSnake.length > 0) {
              greenSnake.pop();
            } else if (dot.color === 'red' && redSnake.length > 0) {
              redSnake.pop();
            } else if (dot.color === 'orange' && orangeSnake.length > 0) {
              orangeSnake.pop();
            }
            break;
          }
        }
        if (!eaten) {
          remainingDots.push(dot);
        } else {
          spawnDot(dot.color);
        }
      }
      dots = remainingDots;

      updateHUD();
      draw();

      // Check win/loss
      if (greenSnake.length === 0) {
        isGameOver = true;
        showOverlay("GAME OVER! Green snake eliminated.");
      } else if (redSnake.length === 0 && orangeSnake.length === 0) {
        isGameOver = true;
        showOverlay("VICTORY! All NPC snakes eliminated!");
      }
    }

    function showOverlay(msg) {
      document.getElementById('overlay-msg').innerText = msg;
      document.getElementById('overlay').classList.remove('hidden');
    }

    function draw() {
      // Clear black background
      ctx.fillStyle = '#000000';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Subtle grid lines
      ctx.strokeStyle = '#111111';
      ctx.lineWidth = 1;
      for (let i = 0; i <= GRID_SIZE; i++) {
        ctx.beginPath();
        ctx.moveTo(i * CELL_PX, 0);
        ctx.lineTo(i * CELL_PX, canvas.height);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(0, i * CELL_PX);
        ctx.lineTo(canvas.width, i * CELL_PX);
        ctx.stroke();
      }

      // Draw dots
      dots.forEach(d => {
        ctx.fillStyle = d.color === 'green' ? '#00ff00' : (d.color === 'red' ? '#ff3333' : '#ff9900');
        ctx.beginPath();
        ctx.arc((d.x + 0.5) * CELL_PX, (d.y + 0.5) * CELL_PX, CELL_PX * 0.35, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1;
        ctx.stroke();
      });

      // Draw Green Snake
      drawSnake(greenSnake, '#00ff00', '#009900');
      // Draw Red NPC Snake
      drawSnake(redSnake, '#ff3333', '#991111');
      // Draw Orange NPC Snake
      drawSnake(orangeSnake, '#ff9900', '#aa5500');
    }

    function drawSnake(segments, headColor, bodyColor) {
      segments.forEach((seg, index) => {
        ctx.fillStyle = index === 0 ? headColor : bodyColor;
        ctx.fillRect(seg.x * CELL_PX + 1, seg.y * CELL_PX + 1, CELL_PX - 2, CELL_PX - 2);
        if (index === 0) {
          ctx.strokeStyle = '#ffffff';
          ctx.lineWidth = 1;
          ctx.strokeRect(seg.x * CELL_PX + 1, seg.y * CELL_PX + 1, CELL_PX - 2, CELL_PX - 2);
        }
      });
    }

    function resetGame() {
      initGame();
      draw();
    }

    window.addEventListener('keydown', e => {
      switch (e.key) {
        case 'ArrowUp':
        case 'w':
        case 'W':
          if (greenDir.y !== 1) nextGreenDir = {x: 0, y: -1};
          e.preventDefault();
          break;
        case 'ArrowDown':
        case 's':
        case 'S':
          if (greenDir.y !== -1) nextGreenDir = {x: 0, y: 1};
          e.preventDefault();
          break;
        case 'ArrowLeft':
        case 'a':
        case 'A':
          if (greenDir.x !== 1) nextGreenDir = {x: -1, y: 0};
          e.preventDefault();
          break;
        case 'ArrowRight':
        case 'd':
        case 'D':
          if (greenDir.x !== -1) nextGreenDir = {x: 1, y: 0};
          e.preventDefault();
          break;
        case 'r':
        case 'R':
          resetGame();
          break;
      }
    });

    initGame();
    draw();
    gameLoopInterval = setInterval(step, 140);
  </script>
</body>
</html>
"""
