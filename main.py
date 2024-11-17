import csv
from datetime import datetime, timedelta, timezone
import discord

ProfileToUidMapping = {
    "Gabe" : 650140370193219594, 
    "Derrick" : 650140370193219594,
    "Ahmed" : 912550670597488661,
}

TOKEN = ""

channel_mapping = {
    1: 1147380412629397585,  # ValorSuccessChannel
    2: 1156836773306048553,  # CyberSuccessChannel
    3: 1200723508368506983,  # AlpineSuccessChannel
    4: 1269784402712461382,  # MakeSuccessChannel
    5: 1288267605647429692,  # SwiftSuccessChannel
    6: 1293669222026842164,  # RefractSuccessChannel
    7: 1288854903174729748  # StellarSuccessChannel
}









# IGNORE ---------------------------------------------------------

processedMessages = []
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def handleValor(message):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    if field.name.lower() == "product":
                        product = field.value
                    elif field.name.lower() == "site":
                        site = field.value
                    elif field.name.lower() == "size":
                        size = field.value
                    elif field.name.lower() == "profile":
                        profile = field.value
                    elif field.name.lower() == "order":
                        order = field.value
                    elif field.name.lower() == "orderlink":
                        orderLink = field.value

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleCyber(message):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.description:
                product = embed.description.split('\n')[0]

            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "store":
                        site = field.value
                    elif field_name == "profile":
                        profile = field.value
                    elif field_name == "order":
                        order = field.value

                        if "[" in order and "]" in order:
                            order.replace("|", "").strip()
                            order_id, order_link = order.split("](")
                            order = order_id[1:].replace("[", "").replace("|", "").strip()
                            orderLink = order_link[:-1].replace(")", "").replace("|", "").strip()

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleAlpine(message):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "site:":
                        site = field.value
                    elif field_name == "size:":
                        size = field.value
                    elif field_name == "profile:":
                        profile = field.value
                    elif field_name == "order:":
                        order = field.value

                        if "[" in order and "]" in order:
                            order.replace("|", "").strip()
                            order_id, order_link = order.split("](")
                            order = order_id[1:].replace("[", "").strip()
                            orderLink = order_link[:-1].replace(")", "").replace("|", "").strip()
                    elif field_name == "product:":
                        if "[" in field.value and "]" in field.value:
                            product_name, _ = field.value.split("](")
                            product = product_name[1:].strip("[")

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleMake(message):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:

            if embed.description:
                site = embed.description.strip()

            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "product":
                        if "[" in field.value and "]" in field.value:
                            product_name, _ = field.value.split("](")
                            product = product_name[1:].strip("[")

                    elif field_name == "size":
                        if not size:
                            size = field.value
                    elif field_name == "profile name":
                        profile = field.value
                    elif field_name == "order":
                        order = field.value
                        # Extract order ID and order link from the order string if applicable
                        if "[" in order and "]" in order:
                            order.replace("|", "").strip()
                            order_id, order_link = order.split("](")
                            order = order_id[1:].replace("[", "").strip()
                            orderLink = order_link[:-1].replace(")", "").replace("|", "").strip()

            if embed.title:
                order = embed.title  # Set order as the title of the embed
            if embed.url:
                orderLink = embed.url  # Set orderLink as the embed URL

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleSwift(message):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.strip().lower()
                    if field_name == "**site**":
                        site = field.value
                    elif field_name == "**item**":
                        product = field.value
                    elif field_name == "**profile**":
                        profile = field.value
                    elif field_name == "**order #**":
                        order = field.value.replace("||", "").strip()
                    elif field_name == "**size**":
                        size = field.value

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleRefract(message):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "product":
                        if "[" in field.value and "]" in field.value:
                            product_name, _ = field.value.split("](")
                            product = product_name[1:].strip("[")
                    elif field_name == "price":
                        pass
                    elif field_name == "profile":
                        profile = field.value
                    elif field_name == "order number":
                        order = field.value
                        # Extract order ID and order link from the order string if applicable
                        if "[" in order and "]" in order:
                            order.replace("|", "").strip()
                            order_id, order_link = order.split("](")
                            order = order_id[1:].replace("[", "").strip()
                            order.replace('|', '').strip()
                            orderLink = order_link[:-1].replace(")", "").replace("|", "").strip()

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

def handleStellar(message):
    product = image = site = size = profile = order = orderLink = ""

    if message.embeds:
        for embed in message.embeds:
            if embed.fields:
                for field in embed.fields:
                    field_name = field.name.lower()
                    if field_name == "product":
                        product = field.value
                    elif field_name == "site":
                        site = field.value
                    elif field_name == "profile":
                        profile = field.value

            if embed.thumbnail:
                image = embed.thumbnail.url or '[No thumbnail URL]'

    values = [product, image, site, size, profile, order, orderLink]
    set_count = sum(bool(value) for value in values)

    if set_count >= 3:
        return (product, site, size, profile, order, orderLink)
    else:
        return None

async def fetch_messages_and_generate_csv():
    num_days = int(input("Enter the number of days to check messages: "))
    
    # Define the time range
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=num_days)

    all_data = []

    for key, channel_id in channel_mapping.items():
        channel = client.get_channel(channel_id)
        last_message = None  # Tracks the last fetched message for pagination

        while True:
            # Fetch the message history in batches
            messages = []
            async for message in channel.history(
                limit=100,
                before=last_message
            ):
                if message.created_at < start_time:
                    break
                
                messages.append(message)
                print(message)
            
            if not messages:  # If no messages are returned, we're done
                break

            for message in messages:
                try:

                    result = None
                    if key == 1:
                        result = handleValor(message)
                    elif key == 2:
                        result = handleCyber(message)
                    elif key == 3:
                        result = handleAlpine(message)
                    elif key == 4:
                        result = handleMake(message)
                    elif key == 5:
                        result = handleSwift(message)
                    elif key == 6:
                        result = handleRefract(message)
                    elif key == 7:
                        result = handleStellar(message)

                    if result:
                        product, site, size, profile, order, orderLink = result
                        uid = None

                        for name, id in ProfileToUidMapping.items():
                            if name in profile:
                                uid = id
                                break

                        timestamp = message.created_at.isoformat()
                        channel_name = channel.name  # Get the channel name

                        # Append the data, including the channel name
                        all_data.append((timestamp, product, order, orderLink, site, size, profile, uid, channel_name))
                except Exception as e:
                    # Log the error and continue
                    print(f"Error processing message {message.id}: {e}")

            # Update the `last_message` to the oldest message in the current batch
            last_message = messages[-1]

    # Write all collected data to a CSV file
    with open("discord_messages.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Add a column for the channel name
        writer.writerow(["Timestamp", "Product", "Order Number", "Order Link", "Site", "Size", "Profile", "UID", "Channel Name"])
        writer.writerows(all_data)

@client.event
async def on_ready():
    await fetch_messages_and_generate_csv()
    await client.close()

client.run(TOKEN)
