import os
import django
from django.conf import settings

from interactions import Client, Intents, listen, File, Embed
from interactions import slash_command, SlashContext
from interactions import Button, ButtonStyle
from interactions.models.discord import Message
from interactions.api.events import Component
from pathlib import Path
from django.utils import timezone

# Danger zone
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quizzbått.settings')
django.setup()

# Now this script or any imported module can use any part of Django it needs.
from ylequizz.models import Exam, Question, DiscoUser, ExamScore

bot = Client(intents=Intents.DEFAULT)
bot.load_extension("interactions.ext.jurigged")

@listen()
async def on_ready():
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@slash_command(name="quizzme", description="Start the Musiktest :)")
async def my_command_function(ctx: SlashContext):
    exam = Exam.objects.first()
    await ctx.send(f"{ctx.author} is doing {exam.name}")
    await ctx.author.send(f"Starting {exam.name}")
    points = 0
    for q1 in exam.questions.all():
        components = [Button(
                label=x.choice_text, 
                style=ButtonStyle.SECONDARY,
                custom_id=x.id,
            ) for x in q1.options.all()]

        if q1.image:
            pa = Path(q1.image.file.__str__())
            file = File(pa)
            embed = Embed()
            embed.set_image(url=f"attachment://{pa.name}")
            msg = await msg.channel.send(q1.question_text, components=components, embeds=embed, files=file)
        else:
            msg = await ctx.author.send(q1.question_text, components=components)
        # Wait for answer
        try:
            used_component: Component = await bot.wait_for_component(components=components, timeout=120)
            # Disable all buttons
            selected_opt = int(used_component.ctx.component.custom_id)
            if selected_opt == q1.correct.id:
                points += 1
            for b in components:
                b.disabled = True
                cid = int(b.custom_id)
                # Mark correct answer green
                if cid == q1.correct.id:
                    b.style = ButtonStyle.GREEN
                elif cid == selected_opt:
                    b.style = ButtonStyle.RED
            await used_component.ctx.edit_origin(components=components)
            
            if q1.description_img:
                pa = Path(q1.description_img.file.__str__())
                file = File(pa)
                embed = Embed()
                embed.set_image(url=f"attachment://{pa.name}")
                msg = await msg.channel.send(q1.description, embeds=embed, files=file)
            else:
                msg = await ctx.author.send(q1.description)


        # on timeout disable buttons, and update user status in DB (@TODO)
        except TimeoutError:
            for b in components:
                b.disabled = True
            await msg.edit(components=components)
            await ctx.author.send("Too slow quizz ended")
            break
    
    # Create user
    u, _ = DiscoUser.objects.get_or_create(discord_id=ctx.author.id, guild_id=ctx.guild.id)
    u.name = ctx.author
    u.save()
    
    es, _ = ExamScore.objects.get_or_create(user=u, exam=exam,guild_id=ctx.guild.id)
    es.score = points
    es.taken = timezone.now()
    es.save()
    
    await ctx.author.send(f"{points}/{exam.questions.count()}")
    await ctx.send(f"{ctx.author} got {points}/{exam.questions.count()} in {exam.name}")

bot.start(settings.BOT_TOKEN)