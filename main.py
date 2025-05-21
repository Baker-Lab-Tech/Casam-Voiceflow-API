import argparse
import json
import requests
import sys
import time
import platform
from typing import Dict, List, Any

class VoiceflowCLI:
    def __init__(self, user_id=None, message_type=None):
        self.api_key = "VF.DM.68121e4841b879c6b17cb621.TJDyOfUFvptKt3hv"
        self.project_id = "680fa8986a7a57031aa81112"
        self.version_id = "680fa8986a7a57031aa81112"  # Set versionID same as projectID
        self.base_url = "https://general-runtime.voiceflow.com"
        self.api_url = "https://api.voiceflow.com/v2"
        self.user_id = user_id or "user-456"  # Use provided user_id or default
        self.message_type = message_type  # Store message_type
        self.session = None
        self.conversation = []  # Store full conversation for transcript
    
    def set_variables(self, variables: Dict[str, Any]) -> bool:
        """Set variables in the user's state before starting a conversation"""
        url = f"{self.base_url}/state/user/{self.user_id}/variables"
        
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.patch(url, headers=headers, json=variables)
        
        if response.status_code >= 200 and response.status_code < 300:
            print(f"Variables successfully set: {json.dumps(variables)}")
            return True
        else:
            print(f"Error setting variables: {response.status_code}")
            print(response.text)
            return False
    
    def start_session(self) -> None:
        """Initialize a new session with the Voiceflow agent"""
        # Set initial variables if message_type is provided
        if self.message_type:
            self.set_variables({"message_type": self.message_type})
        
        url = f"{self.base_url}/state/user/{self.user_id}/interact"
        
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "projectID": self.project_id,
            "action": {
                "type": "launch"
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            self.session = response.json()
            self._process_response(self.session)
            
            # Start a new conversation
            self.conversation = []
        else:
            print(f"Error starting session: {response.status_code}")
            print(response.text)
            sys.exit(1)
    
    def send_message(self, message: str) -> None:
        """Send a message to the Voiceflow agent"""
        # Add user message to conversation
        self.conversation.append({
            "type": "user",
            "timestamp": int(time.time() * 1000),
            "message": message
        })
        
        url = f"{self.base_url}/state/user/{self.user_id}/interact"
        
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "projectID": self.project_id,
            "action": {
                "type": "text",
                "payload": message
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            self.session = response.json()
            self._process_response(self.session)
        else:
            print(f"Error sending message: {response.status_code}")
            print(response.text)
    
    def _process_response(self, response_data: List[Dict[str, Any]]) -> None:
        """Process and display responses from the Voiceflow agent"""
        for trace in response_data:
            trace_type = trace.get("type")
            
            if trace_type == "text":
                message = trace.get('payload', {}).get('message', '')
                print(f"\nVoiceflow: {message}")
                
                # Add assistant response to conversation
                self.conversation.append({
                    "type": "assistant",
                    "timestamp": int(time.time() * 1000),
                    "message": message
                })
            
            elif trace_type == "speak":
                message = trace.get('payload', {}).get('message', '')
                print(f"\nVoiceflow: {message}")
                
                # Add assistant response to conversation
                self.conversation.append({
                    "type": "assistant",
                    "timestamp": int(time.time() * 1000),
                    "message": message
                })
            
            elif trace_type == "end":
                print("\nVoiceflow: Conversation ended.")
                
                # Submit the transcript when conversation ends
                self._submit_transcript()
                sys.exit(0)
    
    def _submit_transcript(self) -> None:
        """Submit transcript to Voiceflow's official Transcript API"""
        # First, try to get project information to find the right version ID
        try:
            self._get_version_id()
        except Exception as e:
            print(f"Warning: Could not get version ID: {str(e)}")
        
        url = f"{self.api_url}/transcripts"
        
        # Keep the full API key for authorization
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }
        
        # Format messages in the required format
        messages = []
        for item in self.conversation:
            if item["type"] == "user":
                messages.append({
                    "type": "user",
                    "text": item["message"],
                    "timestamp": item["timestamp"]
                })
            else:
                messages.append({
                    "type": "assistant",
                    "text": item["message"],
                    "timestamp": item["timestamp"]
                })
        
        # Format transcript for Voiceflow API
        transcript_data = {
            "projectID": self.project_id,
            "versionID": self.version_id,
            "userID": self.user_id,
            "sessionID": self.user_id,
            "messages": messages,
            "os": platform.system(),
            "browser": "CLI",
            "device": platform.machine()
        }
        
       
        response = requests.put(url, headers=headers, json=transcript_data)
        
        if response.status_code >= 200 and response.status_code < 300:
            print("\nTranscript successfully submitted to Voiceflow.")
        else:
            print(f"\nError submitting transcript: {response.status_code}")
            print(response.text)
    
    def _get_version_id(self) -> None:
        """Get the version ID for the project"""
        # For this specific project, versionID should be the same as projectID
        
        print(f"Using version ID: {self.version_id}")
        
        # Commenting out the API call to get version since we're explicitly setting it
        """
        url = f"{self.api_url}/projects/{self.project_id}"
        
        # Use the API key without the "VF.DM." prefix
        api_key = self.api_key.split("VF.DM.")[1] if "VF.DM." in self.api_key else self.api_key
        
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code >= 200 and response.status_code < 300:
            data = response.json()
            if "liveVersion" in data:
                self.version_id = data["liveVersion"]
                print(f"Found live version ID: {self.version_id}")
            else:
                print("No live version found in project data")
        else:
            print(f"Error getting project info: {response.status_code}")
            print(response.text)
        """

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Voiceflow CLI')
    parser.add_argument('--user-id', help='User ID for the Voiceflow session')
    parser.add_argument('--message-type', help='Message type to pass to Voiceflow')
    parser.add_argument('--version-id', help='Version ID for the Voiceflow project (default: production)')
    parser.add_argument('--variables', help='JSON string of variables to set before starting conversation')
    parser.add_argument('--cible', help='Value for the Cible variable')
    args = parser.parse_args()
   
    # Initialize the Voiceflow CLI with command line arguments
    voiceflow = VoiceflowCLI(user_id=args.user_id, message_type=args.message_type)
    
    # Set version ID if provided
    if args.version_id:
        voiceflow.version_id = args.version_id
    
    # Set custom variables if provided
    custom_variables = {}
    if args.variables:
        try:
            custom_variables = json.loads(args.variables)
        except json.JSONDecodeError:
            print("Error: Variables must be a valid JSON string")
            sys.exit(1)
    
    # Add Cible variable if provided
    if args.cible:
        custom_variables["Cible"] = args.cible
    
    if custom_variables:
        print("Setting custom variables...")
        voiceflow.set_variables(custom_variables)
    
    # Start a new session
    print("Starting conversation with Voiceflow agent...")
    voiceflow.start_session()
    
    # Main chat loop
    try:
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Exiting conversation...")
                # Submit transcript before exiting
                voiceflow._submit_transcript()
                break
            
            voiceflow.send_message(user_input)
    except KeyboardInterrupt:
        print("\nExiting conversation...")
        # Submit transcript on keyboard interrupt
        voiceflow._submit_transcript()

if __name__ == "__main__":
    main()