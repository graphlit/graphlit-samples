from other import client

async def handle_publish(description, voice):
    content, error_message = await client.publish_text(description, voice)

    if error_message is not None:
        return None, error_message
    else:
        return content, None
