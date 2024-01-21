define v = Character("Valerie", who_color = "#ffffff")
define mst = Character("???")
define m = Character("Mom", who_color = "#000000")
define da = Character("Dad", who_color = "#000000")
define c = Character("Mr. Cross", who_color = "#057536")
define w = Character("Mr. Wordley", who_color = "#7d490a")
define d = Character("Mr. Delva", who_color = "#752b5f")
define p = Character("Mme. Penny", who_color = "#476fff")

# todo list:
# credits for music on about page (done)
# credits for sound effects 
# edit save screen
# change name colours to be visible
# change game icon
# button click sound effects


label start: 

    stop music
    stop audio
    stop sound
    
    $ late = False
    $ morningtime = "6:30 AM"
    $ sick = False
    $ dressed = False
    $ hair = False
    $ food = False
    $ breakfastlist = ["spring rolls", "red bean paste buns", "sushi", "fried rice"]

    python:
        import random
        Physical = random.randint(1, 20)
        Mental = random.randint(1, 20)
        Social = random.randint(1, 20)

    play sound alarmclock loop fadein 1.0 volume 0.75
    scene black
    
    scene bedroom dim
    with fade
    
    "My physical distress is [Physical]. My mental distress is [Mental]. My social distress is [Social]."

    label dayone:
        "Be-be-be-beep!"
        "Be-be-be-beep!"

        v "{i}Ugh..."
        v "{i}What's that sound...?"
        v "{i}It's too early for this..."

        # Max: 23 mental, 25 physical; min: 3 mental, 0 physical
        menu wakeup:
            "Get up.":
                $ Mental += 3
                $ Physical += -1
                jump awake 
            "Don't get up.":
                $ Mental += -1
                $ Physical += 1
                stop sound
                v "{cps=*0.5}...{/cps}"
                v "Zzz..."
                play sound alarmclock loop volume 0.75
                ".{p}.{p}."
                menu wakeup2:
                    "No, really, get up.":
                        $ Physical += -1
                        $ Mental += 4
                        jump awake 
                    "Keep sleeping.":
                        stop sound
                        $ Mental += -2
                        $ Physical += 2
                        v "Zzz... zzz..."
                        "..."
                        "..."
                        play sound alarmclock loop volume 0.75
                        ".{p}.{p}."
                        menu wakeup3:
                            "Wake up. Now.":
                                $ Physical += 3
                                $ late = True
                                python: 
                                    morningtime = "7:" + str(random.randint(20,40)) + " AM"
                                jump awake

        
    label awake:
        call minlimit 
        stop sound
        "[Physical], [Mental], [Social]"
        play music coldbrew

        v "\"Hhhhhh....\""
        v "\"Unnghhhhh...\""
        v "\"Blehhh...\""
        v "\"Okay, okay, I'm awake...\""
        v "Stumbling blindly out of bed, I fumble around uselessly until I find the light switch."

        scene bedroom light

        v "The light is blinding. I regret turning it on immediately."
        v "A quick glance at the clock shows that it's [morningtime]."

        if late:
            v "Oh my god, how did I sleep in that late?"
            v "Hnn..."
            v "Sometimes it feels like there's a mysterious force controlling me, stopping me from waking up when my alarm first goes off."
            v "What a terrible start to my day..."
        if Physical > 15: 
            $ sick = True
            v "Ugh... I feel physically awful too."
            v "My mouth is dry and I can feel a sneeze coming."
            if late:
                v "It's too late to tell Dad to call in sick for me, though."
                v "I'm sure he and Mom are both already downstairs, impatiently waiting for me to get ready."
            else: 
                v "Unfortunately, this is a pretty frequent occurrence every morning."
                v "I didn't think it was possible to actually be allergic to mornings, but I guess I impress myself."

        v "I can already tell that I'm not going to have a good day today."
        v "\"But the grind stops for no one,\" I mumble with little enthusiasm."
        v "Lethargically, I start getting ready for the day."

        #Min: social 0, physical 0; max social 22, physical 24
        menu morningroutine:
            "I'll..."

            "Get dressed." if not dressed:
                jump getdressed
            "Brush my hair." if not hair:
                jump brushhair
            "Eat breakfast." if not food:
                jump eatfood
            "Pack my things." if dressed and hair and food:
                jump backpack
            
        label getdressed:
            $ dressed = True
            if late: 
                $ Social += 1
                v "I don't really have time to think too hard about my outfit for the day."
                v "I grab at my closet blindly, hoping whatever I end up with looks passable."
            elif sick: 
                v "It's really chilly."
                v "The longer I stare into my closet with my pajamas on, the longer I freeze."
                v "\"Brr...\""
                v "I grab a sweater, deciding to put on as many layers as I can fit on."
            jump morningroutine 
        
        label brushhair:
            $ hair = True
            if late: 
                $ Social += 1
                v "I deeply and sorrowfully regret not re-brushing my hair last night."
                v "With every tangle I have to haphazardly brush through, I'm reminded of how little time I have left to get ready."
                v "\"...Whatever, it looks good enough.\""
                v "Maybe if I tell myself that enough times it'll become true."
            jump morningroutine

        label eatfood:
            $ food = True
            $ Physical -= 2
            if sick:
                $ Physical += 1
                v "My tummy hurts..."
                python:
                    "Valerie" "My dad made me " + breakfastlist[random.randint(0,3)] + " for breakfast, but I don't think I can stomach it all..."
                v "I'll take a few bites, but I definitely can't finish the entire plate."
            
                
            jump morningroutine

    label minlimit:
        if Physical < 0:
            $ Physical = 0
        if Mental < 0:
            $ Mental = 0
        if Social < 0:
            $ Social = 0
        return 
        
        



    #play audio coldbrew loop 


# # The script of the game goes in this file.

# # Declare characters used by this game. The color argument colorizes the
# # name of the character.

# define e = Character("Eileen")


# # The game starts here.

# label start:

#     # Show a background. This uses a placeholder by default, but you can
#     # add a file (named either "bg room.png" or "bg room.jpg") to the
#     # images directory to show it.

#     scene bg room

#     # This shows a character sprite. A placeholder is used, but you can
#     # replace it by adding a file named "eileen happy.png" to the images
#     # directory.

#     show eileen happy

#     # These display lines of dialogue.

#     e "You've created a new Ren'Py game."

#     e "Once you add a story, pictures, and music, you can release it to the world!"

#     # This ends the game.

#     return
