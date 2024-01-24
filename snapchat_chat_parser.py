import collections
import datetime
import html
import json
import operator
import os
import argparse


def export_messages_to_files(parsed_chat_history: dict, output_dir):

    num_distinct_contacts = len(parsed_chat_history.keys())

    print(f"Exporting messages from {num_distinct_contacts} users")

    os.makedirs(output_dir)

    # Sort the messages for each user by timestamp,
    # and then dump them out to a JSON file
    for username in parsed_chat_history.keys():

        # Only export messages if there are any present
        if len(parsed_chat_history[username]) > 0:
            parsed_chat_history[username] = sorted(
                parsed_chat_history[username], key=operator.itemgetter('Created-Timestamp'))

            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

            output_filename = f"{timestamp}_snapchat-chat-history-{username}.json"

            with open(os.path.join(output_dir, output_filename), mode='w', encoding="utf-8") as output_json_file:
                # ensure_ascii=False to make emojis render correctly
                # https://stackoverflow.com/a/52206290/1576548
                json.dump(
                    parsed_chat_history[username], output_json_file, indent=4, ensure_ascii=False)


def parse_chats_from_file(chat_history_filepath, year_created):

    with open(file=chat_history_filepath, mode='r', encoding="utf-8") as json_file:

        full_chat_history = json.load(json_file)

        # Build up a dictionary, where the keys are usernames, and the values are a list of messages either sent or received from that user
        parsed_chat_history = collections.defaultdict(list)

        # The "old" format for snapchat chat history logs is much simpler, so we essentially re-use the existing chat object and just add additional properties to make it easier to read.
        # For the newer format, we ignore most of the original chat object to create our own with only the relevant pieces.

        # Once parsed, the output of the "old" (pre-2024) version should have the same format as the output of the new version.

        if year_created < 2024:

            for chat_type in full_chat_history.keys():

                for chat in full_chat_history[chat_type]:

                    # A chat object looks like:
                    # {'From': '<user>', 'Media Type': 'TEXT', 'Created': '2022-07-22 19:28:21 UTC', 'Text': 'Hello World'}

                    if chat_type.startswith("Received"):
                        username = chat["From"]

                    elif chat_type.startswith("Sent"):
                        username = chat["To"]

                    else:
                        raise ValueError(
                            f"Unknown value for chat type: '{chat_type}'")

                    # To make sorting easier ...
                    unix_timestamp_for_chat = int(datetime.datetime.strptime(
                        chat['Created'], "%Y-%m-%d %H:%M:%S %Z").timestamp())

                    chat["Created-Timestamp"] = unix_timestamp_for_chat

                    message_body = chat["Text"]

                    # Convert symbols like '&#39' into the actual character representation
                    if (message_body is not None):
                        message_body = html.unescape(message_body)

                    parsed_chat_history[username].append(chat)

                print(
                    f"Finished analyzing {len(full_chat_history[chat_type])} {chat_type} messages")

        elif year_created >= 2024:

            # The new chat objects are much easier to work with. They consist of a nested dictionary, where the first level of keys are the senders,
            # and the values are arrays that are all messages between you and that sender.

            # {
            #   "abraham": [ <---- This array has all messages between you and Abraham
            #     {
            #       "From": "abraham",
            #       "Media Type": "TEXT",
            #       "Created": "2024-01-20 06:33:05 UTC",
            #       "Content": null,
            #       "Conversation Title": null,
            #       "IsSender": false,
            #       "Created(microseconds)": 1705732385472
            #     }
            #   ]

            for username in full_chat_history.keys():

                if len(username) > 1:

                    for chat in full_chat_history[username]:

                        new_chat_obj = dict()

                        # There's 2 possible values: "TEXT" for regular text messages and "SHARE" which is usually a story being shared
                        if chat["Media Type"] == "TEXT":

                            if chat["IsSender"] == True:

                                # username = new_chat_obj["To"]
                                new_chat_obj["To"] = username

                            elif chat["IsSender"] == False:

                                # username = chat["From"]
                                new_chat_obj["From"] = username

                            else:
                                raise ValueError(
                                    f"Unknown value for `IsSender` key, expected only true or false, got: {chat['IsSender']}")

                            # Set dates
                            new_chat_obj["Created-Timestamp"] = chat["Created(microseconds)"]
                            new_chat_obj["Created"] = chat["Created"]

                            # Lastly, add the message body if it exists
                            if chat["Content"] is not None and len(chat["Content"]) > 0:
                                new_chat_obj["Text"] = chat["Content"]

                            parsed_chat_history[username].append(new_chat_obj)

                    print(
                        f"Finished analyzing {len(parsed_chat_history[username])} messages from {username}")

        return parsed_chat_history


if __name__ == "__main__":

    argparse_parser = argparse.ArgumentParser()

    argparse_parser.add_argument("-i", "--input-chat-history-json", required=True,
                                 type=str, help="The path to the `chat_history.json` file")

    argparse_parser.add_argument("-y", "--year", required=True, type=int,
                                 help="The year the snapchat dump was taken. Needed to determine format.")

    argparse_parser.add_argument("-o", "--output-dir", required=True,
                                 type=str, help="The output directory to put the JSON files")

    argparse_args = argparse_parser.parse_args()

    chat_history_filepath = argparse_args.input_chat_history_json

    if os.path.exists(chat_history_filepath):

        parsed_chat_history = parse_chats_from_file(
            chat_history_filepath, argparse_args.year)
        export_messages_to_files(parsed_chat_history, argparse_args.output_dir)

    else:
        raise FileNotFoundError(
            f"Error couldn't find chat history file: '{chat_history_filepath}'")
