# AI Business Analytics

A Frappe Framework application that allows users to ask business questions in natural language and retrieve information from a five-year synthetic business dataset.

## 1. Project Overview

This project implements an AI-assisted business analytics interface using Frappe Framework.

Users can enter natural-language questions such as:

- What were the sales for each year?
- Show me sales by city for 2025.
- What is the production status distribution?
- Show revenue by product category for 2025.
- Show customers who recently purchased.

The system interprets the question, maps it to an allowlisted analytics operation, executes a controlled backend query, and displays the result in the Frappe UI.

Unsupported questions are rejected instead of generating unsupported business results.

## 2. Technology Stack

- Frappe Framework
- Python
- MariaDB
- JavaScript
- Ollama
- Qwen 2.5 local LLM
- Docker / Frappe Dev Container
- Git / GitHub

The LLM is hosted locally through Ollama, so no paid external AI API is required.

## 3. Architecture

```text
User
  |
  v
Frappe AI Business Analytics Page
  |
  v
Natural Language Question
  |
  v
Fast Deterministic Classifier
  |
  +---- Supported obvious query ----> Allowlisted Analytics Function
  |
  +---- Complex/indirect query ------> Ollama LLM
                                      |
                                      v
                              Structured Query Plan
                                      |
                                      v
                              Allowlisted Operation
  |
  v
MariaDB
  |
  v
Analytics Result
  |
  v
Frappe UI