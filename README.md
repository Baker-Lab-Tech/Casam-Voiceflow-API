# Voiceflow CLI

A command-line interface for interacting with Voiceflow conversational agents. This tool allows you to have text-based conversations with your Voiceflow chatbot and automatically submits conversation transcripts to Voiceflow's official Transcript API.

## Features

- Interactive chat interface with Voiceflow agents
- Automatic transcript submission
- Custom variable support
- Session management
- Platform and device information tracking
- Support for different message types
- Support for setting Voiceflow variables, including the 'Cible' variable

## Prerequisites

- Python 3.x
- `requests` library

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install requests
```

## Usage

Basic usage:
```bash
python main.py
```

### Command Line Arguments

- `--user-id`: Specify a custom user ID for the Voiceflow session
- `--message-type`: Set a message type to pass to Voiceflow
- `--version-id`: Specify a custom version ID for the Voiceflow project
- `--variables`: Pass custom variables as a JSON string
- `--cible`: Set the value for the 'Cible' variable in Voiceflow

Examples:

```bash
# With custom user ID
python main.py --user-id "user-456"

# With message type
python main.py --message-type "support"

# With custom variables
python main.py --variables '{"name": "John", "preference": "email"}'

# With Cible variable
python main.py --cible "target-value"

# Combining multiple arguments
python main.py --user-id "custom-user" --cible "target-value" --variables '{"language": "french"}'
```

### During Conversation

- Type your messages and press Enter to send them
- To end the conversation, type:
  - `exit`
  - `quit`
  - `bye`
  - Or press Ctrl+C

## Transcript Submission

The tool automatically submits conversation transcripts to Voiceflow's Transcript API when:
- The conversation ends naturally
- The user types an exit command
- The program is interrupted with Ctrl+C

Transcripts include:
- Full conversation history
- Timestamps for each message
- Platform information
- Browser/device details
- Session information

## Setting Variables

The application supports setting Voiceflow variables in two ways:

1. Through the `--variables` argument with a JSON string:
```bash
python main.py --variables '{"name": "John", "age": 30}'
```

2. Through specific command-line arguments for key variables:
```bash
python main.py --cible "target-value"
```

Variables are set before the conversation starts using Voiceflow's variable API.

## Error Handling

The script includes error handling for:
- API request failures
- Invalid JSON input
- Network issues
- Keyboard interrupts

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here] 