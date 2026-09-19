import discord
from discord.ext import commands
from discord.ui import View, Button

# =========================
# CONFIG
# =========================

PREFIX = "&"

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)


# =========================
# VERIFICATION BUTTON
# =========================

class VerificationView(View):
    def __init__(self, verify_role):
        super().__init__(timeout=None)
        self.verify_role_id = verify_role.id

    @discord.ui.button(
        label="Verify",
        style=discord.ButtonStyle.success,
        emoji="✅",
        custom_id="verification_button"
    )
    async def verify(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        guild = interaction.guild
        member = interaction.user

        role = guild.get_role(self.verify_role_id)

        if role is None:
            await interaction.response.send_message(
                "❌ Verification role no longer exists.",
                ephemeral=True
            )
            return

        if role in member.roles:
            await interaction.response.send_message(
                "✅ You are already verified!",
                ephemeral=True
            )
            return

        try:
            await member.add_roles(
                role,
                reason="Member verified through verification system"
            )

            await interaction.response.send_message(
                "🎉 **Verification successful!**\n"
                "You now have access to the server.",
                ephemeral=True
            )

        except discord.Forbidden:
            await interaction.response.send_message(
                "❌ I can't give you the verification role. "
                "Make sure my bot role is above the `@verify` role.",
                ephemeral=True
            )

        except Exception as e:
            print(f"Verification error: {e}")

            await interaction.response.send_message(
                "❌ Something went wrong while verifying you.",
                ephemeral=True
            )


# =========================
# BOT READY
# =========================

@bot.event
async def on_ready():
    print("=" * 50)
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print(f"Servers: {len(bot.guilds)}")
    print("=" * 50)

    # Persistent button
    for guild in bot.guilds:
        role = discord.utils.get(
            guild.roles,
            name="verify"
        )

        if role:
            bot.add_view(
                VerificationView(role)
            )


# =========================
# VERIFICATION SETUP
# =========================

@bot.command()
@commands.has_guild_permissions(administrator=True)
async def verification(ctx, action=None):

    if action is None:
        await ctx.send(
            "❌ Usage:\n"
            "`&verification setup`"
        )
        return

    if action.lower() != "setup":
        await ctx.send(
            "❌ Unknown option.\n"
            "Use `&verification setup`"
        )
        return

    guild = ctx.guild

    setup_message = await ctx.send(
        "⚙️ **Setting up verification system...**"
    )

    # =========================================
    # CREATE / FIND VERIFY ROLE
    # =========================================

    verify_role = discord.utils.get(
        guild.roles,
        name="verify"
    )

    if verify_role is None:

        # Create role below bot's highest role
        verify_role = await guild.create_role(
            name="verify",
            color=discord.Color.green(),
            reason="Verification system setup"
        )

        print(
            f"Created verification role in {guild.name}"
        )

    # =========================================
    # CREATE / FIND VERIFY CHANNEL
    # =========================================

    verify_channel = discord.utils.get(
        guild.text_channels,
        name="verify"
    )

    if verify_channel is None:

        verify_overwrites = {
            guild.default_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                read_message_history=True
            ),

            verify_role: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=False,
                read_message_history=True
            ),

            guild.me: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_messages=True
            )
        }

        verify_channel = await guild.create_text_channel(
            "verify",
            overwrites=verify_overwrites,
            topic="Click the button below to verify yourself.",
            reason="Verification system setup"
        )

        print(
            f"Created #verify in {guild.name}"
        )

    # =========================================
    # LOCK ALL OTHER CHANNELS
    # =========================================

    for channel in guild.channels:

        # Don't lock verification channel
        if channel.id == verify_channel.id:
            continue

        try:

            # ================================
            # TEXT CHANNELS
            # ================================

            if isinstance(channel, discord.TextChannel):

                await channel.set_permissions(
                    guild.default_role,
                    view_channel=False,
                    reason="Verification system"
                )

                await channel.set_permissions(
                    verify_role,
                    view_channel=True,
                    send_messages=True,
                    read_message_history=True,
                    reason="Verification system"
                )

            # ================================
            # VOICE CHANNELS
            # ================================

            elif isinstance(channel, discord.VoiceChannel):

                await channel.set_permissions(
                    guild.default_role,
                    view_channel=False,
                    connect=False,
                    reason="Verification system"
                )

                await channel.set_permissions(
                    verify_role,
                    view_channel=True,
                    connect=True,
                    speak=True,
                    reason="Verification system"
                )

            # ================================
            # CATEGORY
            # ================================

            elif isinstance(channel, discord.CategoryChannel):

                await channel.set_permissions(
                    guild.default_role,
                    view_channel=False,
                    reason="Verification system"
                )

                await channel.set_permissions(
                    verify_role,
                    view_channel=True,
                    reason="Verification system"
                )

        except discord.Forbidden:
            print(
                f"❌ No permission to edit: {channel.name}"
            )

        except Exception as e:
            print(
                f"❌ Error editing {channel.name}: {e}"
            )

    # =========================================
    # SEND VERIFICATION MESSAGE
    # =========================================

    embed = discord.Embed(
        title="🛡️ Server Verification",
        description=(
            "**Welcome!** 👋\n\n"
            "Before accessing the server, "
            "you need to verify yourself.\n\n"
            "Click the button below to get "
            "access to the server.\n\n"
            "╰┈➤ **Click `Verify` to continue.**"
        ),
        color=discord.Color.green()
    )

    embed.set_footer(
        text=f"{guild.name} • Verification System"
    )

    # Delete old bot verification messages
    try:
        async for message in verify_channel.history(limit=50):

            if message.author.id == bot.user.id:
                try:
                    await message.delete()
                except:
                    pass

    except:
        pass

    await verify_channel.send(
        embed=embed,
        view=VerificationView(verify_role)
    )

    # =========================================
    # FINISH
    # =========================================

    await setup_message.edit(
        content=(
            "✅ **Verification setup completed!**\n\n"
            f"🛡️ Role: {verify_role.mention}\n"
            f"🔐 Channel: {verify_channel.mention}\n\n"
            "🔒 All other channels are now locked "
            "for unverified members.\n"
            "✅ Verified members can access them."
        )
    )


# =========================
# ERROR HANDLER
# =========================

@verification.error
async def verification_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "❌ You need **Administrator** permission "
            "to use this command."
        )

    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "❌ Usage: `&verification setup`"
        )

    else:
        print(f"Command error: {error}")

        await ctx.send(
            "❌ An error occurred while running the command."
        )


# =========================
# HELP
# =========================

@bot.command()
async def helpme(ctx):

    embed = discord.Embed(
        title="🛡️ Verification Bot",
        description=(
            "`&verification setup`\n"
            "Set up the complete verification system."
        ),
        color=discord.Color.blurple()
    )

    await ctx.send(embed=embed)


# =========================
# RUN BOT
# =========================

TOKEN = "your bot token"

if TOKEN == "PUT_YOUR_BOT_TOKEN_HERE":
    print("❌ Please put your bot token in TOKEN.")

else:
    bot.run(TOKEN)