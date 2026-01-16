
// Antigravity Tennis - Unreal.js Logic
// This script runs INSIDE the Unreal Engine V8 instance

class TennisGame {
    constructor() {
        this.score = { p1: 0, p2: 0 };
        this.isLive = false;
        console.log("🎾 Antigravity Tennis JS Core Initialized");
    }

    startGame() {
        this.score = { p1: 0, p2: 0 };
        this.isLive = true;
        this.spawnBall();
        console.log("🚀 MATCH STARTED");
    }

    spawnBall() {
        // Logic to spawn BP_Ball at center
        // const ball = GWorld.SpawnActor(BALL_CLASS, {Z: 100});
        // ball.SetPhysicsLinearVelocity({X: 500, Y: 200, Z: 0});
        console.log("Spawned Ball.");
    }

    onGoalScored(player) {
        if (!this.isLive) return;

        if (player === 1) this.score.p1++;
        else this.score.p2++;

        console.log(`GOAL! Score: ${this.score.p1} - ${this.score.p2}`);
        this.updateUI();
        this.resetRound();
    }

    updateUI() {
        // Update the 3D Widget text (requires reference to Widget Actor)
        // const widget = GWorld.FindActorByName("ScoreBoard");
        // widget.SetText(`${this.score.p1} : ${this.score.p2}`);
    }

    startBuildPhase() {
        this.isLive = false;
        console.log("🛠️ BUILD PHASE: 10 Seconds to Mutate Level!");

        // Notify UI of countdown
        // Widget.SetText("BUILD MODE: 10s");

        setTimeout(() => {
            this.startPlayPhase();
        }, 10000);
    }

    startPlayPhase() {
        this.isLive = true;
        this.spawnBall();
        console.log("▶️ ACTION PHASE: MATCH START!");
    }

    resetRound() {
        this.startBuildPhase();
    }
}

// Singleton
const Game = new TennisGame();

// Exports for other scripts/modules
module.exports = Game;
