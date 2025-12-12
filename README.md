# Universal Robots Robot Arm for Warehouse Automation

This repository is a part of a larger project, which demonstrates a warehouse automation system built using three different types of robots; two Universal Robots robot arms, a Tello Edu drone, and a GoPiGo car. All robots communicate via a shared Websocket server, which gets notified of any orders that should be picked up from the warehouse using the project's own e-commerce website. This repository contains the implementation for the first Universal Robots robot arm.

## Technology Stack & Libraries

### Languages 
- **URScript** is used to define the functions that control the Universal Robot (e.g. moving the gripper). It is the native programming language used by and created for Universal Robots. 
- **Python** is used to initialize a TCP/IP connection and send these defined URScript functions to the Universal Robot controller via that connection. The Universal Robot controller then executes these functions. 

### Core Libraries 
- **Socket**: TCP/IP communication with the UR robot controller.
- **Asyncio**: lets code execute asynchronously and helps maintain a responsive websocket connection.
- **Websockets**:

## Installation

