import json

def greeting() -> dict:
  """A static default greeting that is sent to the user."""

  FIRST_NAME = context.variables["customer_profile"]["customer_first_name"]
  return {
      "greeting": f"Hi there! Welcome to Cymbal Garden! Is this {FIRST_NAME}?"
      }
