# Robot Arm Technology Research

## Executive Summary

The project has two different problems:

1. Simulate a robot arm accurately and interactively.
2. Convert a human device, later called a "bracelet", into safe robot commands.

These should not be treated as one product. A simulator is not automatically a
hardware driver, and a learning framework is not automatically a robot
controller.

The first decision is therefore:

> Choose the simulator and learning stack first. Add the real device through a
> small adapter after its exact model and SDK are known.

## The Technology Layers

### Physics engine

This calculates bodies, joints, gravity, collisions, friction, contact forces,
and motors.

- MuJoCo is a physics engine.
- PhysX is the physics engine used by Isaac Sim.

### Simulation and robotics framework

This provides environments, robot assets, sensors, controllers, resets,
randomization, and learning interfaces.

- Isaac Sim is NVIDIA's large robotics simulation application built around
  Omniverse and PhysX.
- Isaac Lab is a robot-learning framework built on Isaac Sim.
- MuJoCo does not provide an equivalent all-in-one application layer, although
  it has Python bindings, examples, model assets, and learning integrations.

### Middleware

This moves commands and measurements between programs and hardware.

- ROS 2 is the most common robotics middleware option.
- WebSockets, serial, Bluetooth, and vendor SDKs can also be used.

### Human input device

The device might provide position, orientation, buttons, force, IMU data, EMG
signals, or some combination. The word "bracelet" is not enough to choose an
integration method.

## MuJoCo

### What it is good at

- Fast, lightweight local simulation.
- Direct Python and C APIs.
- Articulated robot dynamics and contact-rich manipulation.
- Low-latency control loops.
- Easy inspection of joint positions, velocities, contacts, forces, and
  end-effector Jacobians.
- Simple model files using MJCF XML.
- Good support for custom controllers, sensors, actuators, callbacks, and
  plugins.
- Curated robot models through MuJoCo Menagerie, including Franka, UR arms,
  KUKA, xArm, Sawyer, ALOHA, and others.
- Easier debugging because the application is small and the physics loop is
  visible to us.

### What it is not good at

- It does not provide the same batteries-included learning workflow as Isaac
  Lab.
- It does not automatically solve hardware integration.
- Realistic large environments and photorealistic sensor simulation require
  more work.
- We must build more of the task, data collection, device mapping, and policy
  workflow ourselves.
- GPU versions are mainly useful for many parallel training environments, not
  automatically better for one interactive arm.

### MuJoCo GPU options

- MJX uses JAX and is useful for batched simulation and differentiable learning
  in supported features.
- MuJoCo Warp targets NVIDIA GPU throughput and large batches.
- Regular MuJoCo is usually the better choice for one low-latency interactive
  simulation or teleoperation loop.

## NVIDIA Isaac Lab and Isaac Sim

### What they are good at

- Ready-made robot-learning environments.
- Franka, UR10, dexterous-hand, humanoid, and contact-rich manipulation tasks.
- Built-in task configuration, resets, observations, actions, rewards, and
  domain randomization.
- Reinforcement learning with several supported libraries.
- Imitation learning and demonstration recording.
- Cameras, depth, segmentation, ray sensors, contact sensors, and other
  simulated sensors.
- GPU-parallel training across many environments.
- Higher-quality rendering and synthetic-data workflows.
- More direct NVIDIA ecosystem support for sim-to-real research.

### What they are not good at

- Much heavier installation and runtime requirements.
- More memory, GPU, disk, and driver sensitivity.
- More layers to debug: Isaac Lab, Isaac Sim, Omniverse Kit, extensions,
  PhysX, Python environments, and learning libraries.
- A feature working in Isaac Lab generally does not mean every platform or
  operating system supports it.
- Single-arm interactive control can be unnecessarily complex if we do not
  need cameras, massive parallelism, or learning.
- Some teleoperation and imitation features are Linux-first or Linux-only.

### Windows reality

Isaac Sim and Isaac Lab generally support Windows 11. That does not guarantee
that every teleoperation, imitation-learning, ROS 2, or vendor SDK workflow
works equally well on Windows. Each required feature must be checked
individually.

The current computer has an RTX 3090, which is a reasonable Isaac Sim class of
GPU, but Isaac Sim also depends on driver versions, RAM, storage, and VRAM.

## Direct Comparison

| Requirement | MuJoCo | Isaac Lab / Isaac Sim |
|---|---|---|
| First simple arm simulation | Better | More setup than necessary |
| Low-latency interaction | Better | Possible, but heavier |
| Contact and joint inspection | Better and simpler | Strong, with more layers |
| Photorealistic cameras | Limited | Better |
| Ready-made manipulation tasks | Moderate | Better |
| Reinforcement-learning throughput | Good with MJX/Warp | Excellent and integrated |
| Imitation-learning workflow | Must assemble | Better built-in workflow |
| Custom hardware bridge | Easier to control directly | Possible, but integration is heavier |
| Haptic feedback loop | Easier to keep lean | Strong if the supported device path matches |
| Windows simplicity | Better | More risk |
| Linux robotics ecosystem | Good | Usually best-supported |
| Learning curve | Smaller | Larger |
| Compute requirements | Low to moderate | High |

## The Human Device Problem

There are four very different possibilities:

### Haptic controller

Examples include a device that tracks a tool in 3D and can push back with
force. This is not normally worn like a bracelet. It needs a high-rate loop,
careful force limits, and a connection to the simulator's contact forces.

### IMU bracelet

This provides orientation and acceleration, but not absolute position. It is
useful for gestures or relative motion, but it cannot directly describe a full
end-effector pose without calibration, filtering, and drift correction.

### EMG bracelet

This measures muscle activity. It does not directly provide robot pose. A
machine-learning or signal-processing layer must classify intent before the arm
can be controlled.

### Custom or unknown device

We need the vendor, model, SDK, transport, sampling rate, signal types, and
whether it supports force feedback before making a technology decision.

## Recommended Architecture

Keep the hardware independent from the simulator:

```text
human device
    -> device adapter
    -> normalized command message
    -> safety and workspace filter
    -> IK or robot controller
    -> simulator
    -> state/contact feedback
    -> device feedback adapter
```

The normalized command should eventually contain:

- timestamp
- position, if available
- orientation, if available
- linear and angular velocity, if available
- buttons or gripper intent
- confidence or signal-quality value
- source and connection status

The simulator should never trust raw hardware input directly. It must enforce
workspace limits, joint limits, velocity limits, acceleration limits, and a
disconnect timeout.

## Practical Recommendation

### Choose MuJoCo first when

- The immediate goal is to understand robot-arm physics.
- We need interactive control and low latency.
- The bracelet is unknown.
- We want to run comfortably on Windows.
- We want to inspect and debug every control step.

### Choose Isaac Lab first when

- The main goal is reinforcement learning or imitation learning.
- We need many parallel environments.
- We need realistic camera data or synthetic data.
- The exact teleoperation device is already supported.
- We can use Linux if a required feature is Linux-only.

### Current recommendation for this project

Do not choose Isaac Lab merely because it is NVIDIA, and do not choose MuJoCo
merely because it is already installed.

Use MuJoCo as the initial research and control reference because it is simpler,
already works in this repository, and is suitable for testing an unknown input
device. Reconsider Isaac Lab when the project requirements prove that built-in
imitation learning, camera simulation, or large-scale GPU training are needed.

This is a staged decision, not a permanent rejection of Isaac Lab.

## What Must Be Known Before More Code

1. Exact bracelet/device name and vendor.
2. Whether it gives pose, IMU, EMG, buttons, force, or only gestures.
3. Whether the first goal is teleoperation, demonstration recording, or learned
   control.
4. Which arm model the project must represent.
5. Whether Linux is available if Isaac Lab requires it for the chosen workflow.
6. Whether cameras and photorealism are actual requirements or distractions.

## Sources

- MuJoCo overview: https://mujoco.readthedocs.io/en/stable/overview.html
- MuJoCo simulation and control: https://mujoco.readthedocs.io/en/stable/programming/simulation.html
- MuJoCo model gallery: https://mujoco.readthedocs.io/en/stable/models.html
- MuJoCo GPU backends: https://mujoco.readthedocs.io/en/stable/mjwarp/index.html
- Isaac Lab: https://isaac-sim.github.io/IsaacLab/main/
- Isaac Lab environments: https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html
- Isaac Lab imitation learning: https://isaac-sim.github.io/IsaacLab/main/source/overview/imitation-learning/teleop_imitation.html
- Isaac Sim requirements: https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html
- Isaac Lab Haply teleoperation: https://isaac-sim.github.io/IsaacLab/main/source/how-to/haply_teleoperation.html