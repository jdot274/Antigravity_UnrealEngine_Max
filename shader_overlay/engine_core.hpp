#ifndef CORE_ENGINE_H
#define CORE_ENGINE_H

#include <vector>
#include <string>
#include <map>
#include <iostream>

// Simple JSON-like structure for bridge
struct ActorData {
    std::string id;
    std::string type;
    float posX, posY, posZ;
    float scaleX, scaleY, scaleZ;
    bool hasPhysics;
};

class RenderingPipeline {
public:
    void ProcessPythonInput(const std::string& jsonData) {
        // In a real scenario, use a JSON parser like nlohmann/json
        std::cout << "[C++ Engine] Received Python Command: " << jsonData << std::endl;
        UpdateInternalState();
    }

    void UpdatePhysics(float deltaTime) {
        // C++ Physics Step - optimized for heavy scene actors
        for (auto& actor : sceneActors) {
            if (actor.hasPhysics) {
                actor.posY -= 9.81f * deltaTime; // Simple gravity
            }
        }
    }

    void AddActor(const ActorData& data) {
        sceneActors.push_back(data);
        std::cout << "[C++ Engine] Actor Added: " << data.type << " at ID " << data.id << std::endl;
    }

private:
    void UpdateInternalState() {
        // Internal pipeline sync
    }

    std::vector<ActorData> sceneActors;
};

#endif
