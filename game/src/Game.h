#pragma once

#include <string>
#include <chrono>

class Game {
public:
    Game();
    ~Game() = default;

    void run();

private:
    void init();
    void processInput();
    void update(float deltaTime);
    void render();
    void cleanup();

    bool m_running;
    int  m_tickCount;

    std::chrono::steady_clock::time_point m_lastTime;
};
