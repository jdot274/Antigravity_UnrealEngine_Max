#include "Game.h"

#include <iostream>
#include <thread>
#include <chrono>

Game::Game()
    : m_running(false)
    , m_tickCount(0)
{}

void Game::run()
{
    init();

    m_lastTime = std::chrono::steady_clock::now();

    while (m_running) {
        auto now      = std::chrono::steady_clock::now();
        float delta   = std::chrono::duration<float>(now - m_lastTime).count();
        m_lastTime    = now;

        processInput();
        update(delta);
        render();

        // Cap at ~60 ticks/sec
        std::this_thread::sleep_for(std::chrono::milliseconds(16));
    }

    cleanup();
}

void Game::init()
{
    std::cout << "=== C++ Game Initialized ===\n";
    std::cout << "Press ENTER to advance a tick, or type 'q' + ENTER to quit.\n\n";
    m_running = true;
}

void Game::processInput()
{
    // Non-blocking stdin check: peek without blocking
    // For Replit (terminal), we just read a full line when the loop calls here.
    // The loop is gated by the sleep, so input is buffered naturally.
    // A real game would use ncurses or SDL; this keeps zero dependencies.
}

void Game::update(float deltaTime)
{
    (void)deltaTime; // suppress unused warning
    ++m_tickCount;

    // Read a line of user input each tick
    std::string line;
    if (!std::getline(std::cin, line)) {
        m_running = false;
        return;
    }

    if (line == "q" || line == "Q") {
        m_running = false;
    }
}

void Game::render()
{
    if (!m_running) return;
    std::cout << "[Tick " << m_tickCount << "] Game is running. (q = quit)\n";
}

void Game::cleanup()
{
    std::cout << "\n=== Game Over — total ticks: " << m_tickCount << " ===\n";
}
