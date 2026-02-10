from enum import Enum
import json

class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"

print(f"RoleEnum.assistant value: {RoleEnum.assistant}")
print(f"Type: {type(RoleEnum.assistant)}")
print(f"Is instance of str? {isinstance(RoleEnum.assistant, str)}")
print(f"str(RoleEnum.assistant): {str(RoleEnum.assistant)}")
print(f"Equal to 'assistant'? {RoleEnum.assistant == 'assistant'}")

# Simulate Pydantic/JSON serialization
data = {"role": RoleEnum.assistant}
try:
    print(f"JSON dump: {json.dumps(data)}")
except Exception as e:
    print(f"JSON dump failed: {e}")
