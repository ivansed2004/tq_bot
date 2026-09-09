# Telegram Queuing Bot

Telegram Queuing Bot (further, simply Bot) is a telegram bot for autoscheduling queues for university routines related to completion of laboratory and practice works keeping order which students were stay in. \
**THE PROJECT IS ARCHIVED. NO SUPPORT ANYMORE.**

## Content
0. Purpose and idea;
1. Stack and dependencies;
2. Concepts: \
   2.1. Queue; \
   2.2. Discipline; \
   2.3. User; \
   2.4. OACJobs;
3. Overall architecture;
4. Database schema;
5. OAC architecture (OAC State Machine);
6. Key functionality: \
   6.1. Autoscheduling; \
   6.2. Notifications;
7. File structure: \
   7.1. tq_bot_service file structure; \
   7.2. gateway_api service file structure;
8. External resources;
9. CI/CD pipeline;
10. Security risks;
11. User actions

## 0. Purpose and idea

Even though each student has its unique number in the group's list, the final order is up to students themselves. To avoid conflicts in opinions between students, the decision to automate the process of queuing has been made.

The purpose of the developing the project was to automate:
1. Opening, activating, closing queues when the time of practice or laboratory lesson came;
2. Scheduling queues;
3. Notifying users when the lesson starts to motivate them to take their places.

The Bot also supports the additional functions like ability to subscribe/unsubscribe the queues if a user wishes.

## 1. Stack and dependencies

All dependencies are specified in $requirements.txt$ file. The key ones are described below:
1. **python-telegram-bot**. Pure-Python asynchronous library that provides a clean and intuitive interface for the Telegram Bot API. Designed around Python's asyncio framework. Allows to build stateful conversational applications.
2. **aiohttp**. Asynchronous HTTP client and server framework built natively on top of Python's asyncio event loop. It is a foundational library for modern async web development in Python, eliminating the need for multi-threading to handle high I/O concurrency.
3. **APScheduler**. Task scheduling library that allows Python applications to execute periodic or time-delayed jobs. It abstracts the complexities of time management, providing a unified interface to run Python functions at specific intervals or pre-defined cron-like times.

## 2. Concepts

### 2.1. Queue
A scheduling unit in a Bot. That's where students can take their place to wait.
### 2.2. Discipline
A 'source of truth' for a queue. It provides an information for users of which lesson they're expecting.
### 2.3. User
A subject that operates on queues. Any authenticated user accesses all the queues in a Bot.
### 2.4. OACJobs
An auxiliary object that stores a queue job state. Initially, the scheduling mechanism in APScheduler does not allows to save the job when the service falls. Having OACJobs as a separated database object is necessary to restore a queue job state.

## 3. Overall architecture

<img width="868" height="446" alt="Screenshot from 2026-09-09 09-14-59" src="https://github.com/user-attachments/assets/90313218-fd06-4744-8db7-97b6775be4fe" />

### 3.1. tq_bot service

The main Bot's service providing key functionality: scheduling, autoscheduling, notifications, access to queues.

### 3.2. gateway_api service

The Bot's service that acts as a intermediary between **tq_bot** service and **postgres**. It exposes API endpoints to **tq_bot** service via FastAPI and ORM for mapping Python objects to relational tables rows to **postgres** service.

### 3.3. postgres service

The Bot's service that interacts with database. Real data are stored in a Docker volume.

## 4. Database schema

<img width="724" height="698" alt="Screenshot from 2026-09-09 09-50-45" src="https://github.com/user-attachments/assets/5a264ace-822b-430e-af49-1cb0c9f5baa3" />

## 5. OAC Architecture (OAC State Machine)

Below is the visual demonstration of OAC State Machine.

<img width="407" height="424" alt="Screenshot from 2026-09-09 10-17-07" src="https://github.com/user-attachments/assets/5fb5c204-d351-4ee4-aaec-436882bdb377" />

According to this architecture, each queue acts as a finite state machine which state is changed at the scheduled time.
The following explains the sense of each state.

### 5.1. Opened State

A queue goes to **opened state** 10 minutes before a lesson, associated with the queue, starts.

### 5.2. Active State

A queue goes to **active state** at the time a lesson starts. Students are still possible to take its place in a queue.

### 5.3. Closed State

A queue goes to **closed state** at the time a lesson ends. Students aren't able to take a place anymore within a week. Order information (the line in which students stay) is erasured.

## 6. Key functionality

### 6.1. Autoscheduling

// on start, on restart \
// manual scheduling allowed

### 6.2. Notifications

// subscriptions, unsubscriptions \
// notifying according to the scheduling time

## 7. File structure

### 7.1. tq_bot service file structure

// Responsibility

### 7.2. gateway_api service file structure

// Responsibility

## 8. External resources

The university's timetable has no public API.

## 9. CI/CD pipeline

// Dockerfile \ 
// Deployment environment (Linux) \
// CI/CD

## 10. Security risks

// Registration on enter (without OAuth, Tokens, etc.) \
// No 2FA authentication \
// The project was local and no need to advances security measures \
// Bot token

## 11. User actions

// How a user can interact with a project
