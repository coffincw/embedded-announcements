# Embedded Announcements Discord Bot
Discord bot for formatting announcements to large public discords

[Invite bot to server](https://discordapp.com/oauth2/authorize?client_id=562863006946689024&permissions=518208&scope=bot)

## Commands
- e!channel [#channel]
    - Sets the specified channel as the target channel for the announcements to be posted to
- e!preview
    - Outputs a preview of the current announcement (to the requesting members current channel)
- e!post
    - Posts the announcement to the set channel
- e!create [contents]
    - Creates an anouncement with the specified contents
    - Content Formatting
        - Title: The first part of your input is the title of the announcement, | should be put at the end of the title and any field. In the input: `e!create Contest | Details<This is a test` The title is `Contest`
        - Sections: Also known as fields when concerning embedded messages.  Separate sections with the '|' character.
        - Section Headers: Section headers are the first few words after a '|' before a < in inputed\nIn the input: `e!create Contest | Other Details<The event will take place...` 'Other Details' would be the header',
        