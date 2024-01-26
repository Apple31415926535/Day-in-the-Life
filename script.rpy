## Everything that actually happens in-game is in this script file!
## Thus, everything in here (comments and code) was written by Valerie unless otherwise specified.

## Names of major characters/characters who speak enough to warrant a shortcut.
define v = Character("Valerie", who_color = "#ffffff")
define dad = Character("Dad")
define mom = Character("Mom")
define cm = Character("Classmate")
define s = Character("Siya")
define gg = Character("GeoGuessr")
define c = Character("Mr. Cross", who_color = "#057536")
define w = Character("Mr. Wordley", who_color = "#7d490a")
define d = Character("Mr. Delva", who_color = "#752b5f")
define p = Character("Mme. Penny", who_color = "#476fff")

####

## Never actually ended up using this since I felt the game was too simple to warrant an intro screen/animation/etc.,
## but I thought it was neat that Ren'Py had this label specifically for showing events before the main menu
# label before_main_menu:

label start: 
    ## Turn off the quick menu for the intro.
    $ quick_menu = False

    ## A special character defined by default by Ren'Py, displaying text in the center of the screen
    ## and hiding the text window. 
    centered "Welcome to Valerie Simulator!"
    centered "Live through a day of Valerie's life, and make her decisions for her!"
    centered "Avoid increasing her {u}physical{/u}, {u}mental{/u}, and {u}social{/u} stress..."
    centered "Or else something bad might just happen!"
    centered "Have fun, and please enjoy..."
    ## argument hard forces the user to wait
    $renpy.pause(delay = 0.75, hard = True)
    centered "{size=+20}{cps=*0.2} A Day In The Life"
    $renpy.pause(delay = 0.5, hard = True)

    ## Stop main menu music in preparation for upcoming SFX.
    stop music
    stop audio
    stop sound
    
    ## Variables to be used to set up flags for certain events, statuses, etc.
    ## Ren'Py uses $ to denote a single-line python statement (like defining a variable)

    $ late = False ## gives you a few extra dialogue lines and changes around the morning activities
    $ sick = False ## the main part that impacts your Physical status. If you're not sick at the beginning, it's likely that your Physical will remain low all game
    
    ## Variables that check off if a player has already seen a given choice
    $ dressed = False 
    $ dream = False
    $ hair = False
    $ food = False
    
    $ physicsq = False ## If asked to answer the physics question, "I don't know" will be an option while physicsq is false
    $ headache = False ## Gives extra dialogue, and has a chance to let the player take a sick day (skips the rest of the school day after history)
    $ techflags = 0 ## If all possible techflags are collected by tech class, player will be redirected to the Enlightened Valerie ending
    $ geopoints = 0 ## Determines end result of GeoGuessr minigame

    ## Variables that check off if a player has already seen a given choice
    $ stay = False 
    $ run = False
    $ shell = False
    $ cariacture = False
    $ character = False

    $ yum = False ## Keep working will be an option in tech class while yum is false, also adds an extra line of dialogue
    $ lemot = "" ## Makes lemot a global variable 
    $ teapoints = 0 ## Tracks how much Valerie likes the user's bubble tea order if player chooses to go the mall
    $ ban = False ## Stops the player from getting the Super Good or Good endings when True (becomes true if player takes sick day)

    ## If the player passes the tech class checkpoint and does not take the bad ending, 
    ## goodboypoints gain precedence over stats to determine the player's ending.
    $ goodboypoints = 0
    
    ## Fun little easter egg—if player wakes up late, morningtime will be set to a later time.
    $ morningtime = "6:30 AM"

    ## Used renpy's randint function to generate physical, mental, and social stress at the beginning of the game at a range of 5-20.
    ## Notably, renpy's randint is superior to python's in the context of most visual novels because they support rollback:
    ## That is to say, if you choose the 'back' button to replay some text, the values stay the same.
    ## Latechance gives the user a 50% chance of having the late status if they sleep in once.
    
    $ Physical = renpy.random.randint(5, 20)
    $ Mental = renpy.random.randint(5, 20)
    $ Social = renpy.random.randint(5, 20)

    $ latechance = renpy.random.randint(2,3)

    ## Loops the alarm clock sound with a one-second fade in at 65% volume.
    play sound alarmclock loop fadein 1.0 volume 0.65
    scene black
    $ quick_menu = True

    ## Fade arguments: how long it takes to fade, hold, and then fade into the scene
    scene bedroom dim with Fade(0.5, 1.0, 0.5)

    ## A custom screen (see screens.rpy) that allows multiple stats to be notified in sequence
    ## as opposed to the default with renpy.notify, which has notification times overlap.
    ## Unlike the dialogue (i.e. v "My phys. stress is [Physical]"), multinotify (and notify) don't make use of Ren'Py's built-in features(?)
    ## so you have to cast stats to strings in order to display them properly
    show screen multinotify(["Physical stress: " + str(Physical), "Mental stress: " + str(Mental), "Social stress: " + str(Social)])

    ## The game dialogue actually starts here.
    label dayone:
        "Be-be-be-beep!"
        "Be-be-be-beep!"

        v "{i}Ugh..."
        v "{i}What's that sound...?"
        v "{i}It's too early for this..."

        ## Choice menu
        menu wakeup:
            "Get up.":
                $ Mental += 3
                $ Physical += -1 
                ## Any time a stat is subtracted from, call minlimit to make sure the value does not go below 0.
                call minlimit from _call_minlimit
                show screen multinotify(["Physical stress -1: " + str(Physical), "Mental stress +3: " + str(Mental)])
                ## 'jump' to the label awake (skip everything preceding it) - jump will be used a lot because of the nature of visual novel pathing.
                jump awake 
            "Don't get up.":
                $ Mental += -1
                $ Physical += 1
                call minlimit from _call_minlimit_1
                show screen multinotify(["Physical stress +1: " + str(Physical), "Mental stress -1: " + str(Mental)])

                ## CPS (see options.rpy) is the speed at which the text shows up.
                ## By default, a player can click to immediately see all the text,
                ## but sometimes it allows for more stylistic choices (like here) 
    
                v "{cps=*0.5}...{/cps}"
                v "Zzz..."
                ".{w}.{w}."
                menu wakeup2:
                    "No, really, get up.":
                        $ Physical += -1
                        $ Mental += 4
                        call minlimit from _call_minlimit_2
                        show screen multinotify(["Physical stress -1: " + str(Physical), "Mental stress +4: " + str(Mental)])
                        if latechance % 2 == 0:
                            $ late = True
                            $ morningtime = "7:" + str(renpy.random.randint(20,40)) + " AM"
                        jump awake 
                    "Keep sleeping.":
                        stop sound
                        $ Mental += -2
                        $ Physical += 2
                        call minlimit from _call_minlimit_3
                        show screen multinotify(["Physical stress +2: " + str(Physical), "Mental stress -2: " + str(Mental)])
                        v "Zzz... zzz..."
                        "..."
                        "..."
                        ".{w}.{w}."
                        menu wakeup3:
                            "Wake up. Now.":
                                $ Physical += 3
                                $renpy.notify("Physical stress +3: " + str(Physical)) 
                                $ late = True
                                
                                $ morningtime = "7:" + str(renpy.random.randint(20,40)) + " AM"
                                jump awake
                                

    label awake: 
        stop sound
        play music coldbrew

        v "\"Hhhhhh....\""
        v "\"Unnghhhhh...\""
        v "\"Blehhh...\""
        v "\"Okay, okay, I'm awake...\""
        v "Stumbling blindly out of bed, I fumble around uselessly until I find the light switch."

        play sound lightswitch

        ## Bedroom dim is bedroom light with a multiply layer on top of it
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

        ## Allows for the immersive visual novel experience of getting to choose what to do,
        ## even though you'll be sent back to the same menu every time.
        ## Removes choices after you've chosen them.
        menu morningroutine:
            "{cps=0}I'll..."

            "Get dressed." if not dressed:
                jump getdressed
            "Brush my hair." if not hair:
                jump brushhair
            "Eat breakfast." if not food:
                jump eatfood
            "Write down the dream I had." if not dream and Social > 15 and Mental > 15 and not late:
                jump dreamjournal
            "Pack my things." if dressed and hair and food:
                jump backpack
            
        label getdressed:
            $ dressed = True
            scene bedroom light
            if late: 
                $ Social += 1
                v "I don't really have time to think too hard about my outfit for the day."
                v "I grab at my closet blindly, hoping whatever I end up with looks passable."
                $renpy.notify("Social stress +1: " + str(Social))
                v "Hurriedly getting dressed, my mind is occupied on what I have to do next."
            elif sick: 
                v "It's really chilly."
                v "The longer I stare into my closet with my pajamas on, the longer I freeze."
                v "\"Brr...\""
                v "I grab a sweater, deciding to put on as many layers as I can fit on."
                v "I wish I could go back to bed, but unfortunately I have to keep getting ready. Next, I'll..."
            else:
                $ Social -= 1
                call minlimit from _call_minlimit_4 
                v "I stare down the articles of clothing in my closet."
                v "Which will have the honour of being worn by me today?"
                v "\"Hmm... you!\"" with vpunch
                v "I snatch some clothes out, satisfied with my outfit coordination."
                $renpy.notify("Social stress -1: " + str(Social))
                v "Next, I'll..."
            jump morningroutine 
        
        label brushhair:
            $ hair = True
            scene bedroom light
            if late: 
                $ Social += 1
                v "I deeply and sorrowfully regret not re-brushing my hair last night."
                v "With every tangle I have to haphazardly brush through, I'm reminded of how little time I have left to get ready."
                v "\"...Whatever, it looks good enough.\""
                v "Maybe if I tell myself that enough times it'll become true."
                $renpy.notify("Social stress +1: " + str(Social))
                v "It's so tiring having to dash from place to place just to get ready in the morning."
                v "Anyway, next up, I'll..."
            else:
                v "I take my time unbraiding my hair from the mess that it became while I was sleeping."
                v "I know I'm fighting a losing battle every time I try to defeat all the knots and tangles..."
                v "But it's nice to sit down in the morning, even for a few minutes, and focus on the repetitive motion of re-braiding."
                v "A brief moment of respite passes, and then it's back to the grueling struggle."
                v "Up next..."
            jump morningroutine

        label dreamjournal:
            $ dream = True

            ## This secret choice was supposed to lead to a secret ending, but I had to scrap it because I was running low on time.
            scene bedroom light
            v "I had a really weird dream last night."
            v "What was it about again...?"
            menu dreamchoices:
                "A death game.":
                    
                    v "Oh yeah, that's right..."
                    v "There were 50 children on a hill who wouldn't behave while playing, and got punished as a result."
                    v "They were struck by a plague that caused them all to rip each other apart while they suffered severe side effects."
                    v "I was the only one who got away, but I knew whoever created the sickness was watching me the whole time home."
                    v "Sounds ominous."
                    v "I'll write it down in my Google Sheet for dreams."
                    v "I think more people should write about their dreams. It's kinda fun to look back on what I was dreaming about a few months ago and wonder what my consciousness was up to."
                "A test.":
                    
                    v "Oh... yeah, that's right..."
                    v "Can't stop thinking about school even in my dreams, I guess."
                    v "That leaves a pretty awful taste in my mouth..."
                    v "I think I was in my middle school classroom?"
                    v "I was the last one to finish my test, but for some reason everyone was waiting for me to finish before they left."
                    v "Somehow I already knew I was going to do badly, but as I went on, a spotlight began to shine on me."
                    v "It was stressful, to say the least."
                    v "I'll write it down in my Google Sheet for dreams, anyway."
                    v "I think more people should write about their dreams. It's kinda fun to look back on what I was dreaming about a few months ago and wonder what my consciousness was up to."
                "A love story.":
                    
                    v "Mmm... yeah, that's right."
                    v "I think I was helping one of my classmates get together with someone?"
                    v "It felt like a fairytale-like environment, though."
                    v "Guess I was happy to third-wheel for the prince and princess."
                    v "Maybe I should read a little less rofan if it's starting to leak into my dreams..."
                    v "It's such an effective form of escapism, though."
                    v "I'll write it down in my Google Sheet for dreams, anyway."
                    v "I think more people should write about their dreams. It's kinda fun to look back on what I was dreaming about a few months ago and wonder what my consciousness was up to."
            
            jump morningroutine

        label eatfood:

            scene notmyactualkitchen:
                zoom 1.5
            $ food = True
            $ Physical -= 2
            call minlimit from _call_minlimit_5
            $renpy.notify("Physical stress -2: " + str(Physical))
            if sick:
                $ Physical += 1
                v "My tummy hurts..."
                v "My dad made me spring rolls for breakfast, but I don't think I can stomach it all..."
                v "I'll take a few bites, but I definitely can't finish the entire plate."
                $renpy.notify("Physical stress +1: " + str(Physical))
                v "\"Ugh..\""
                v "What's next?"
            elif late: 
                v "I manage to get a few bites in to my breakfast before making a break for it."
                v "It's more important that I have my lunch packed for school, anyway."
                v "I can just buy food from the cafeteria if I'm still hungry."
                v "...Even if my stomach is grumbling in protest."
                dad "\"Valerie, are you ready to go yet?\""
                v "!!"
                v "\"In a bit!\""
                v "I definitely have to pick up the pace."
                v "Too much on my plate. Literally."
                v "Next..."
            else:
                v "I chew thoughtfully on the food at the table."
                v "I mean, I don't particularly care for it, but going to school on an empty stomach is never fun."
                v "While I'm in the kitchen, I pack my lunch."
                v "I throw in an extra granola bar for moral support. I deserve a treat."
                v "Next on the list of things to do..."              
            jump morningroutine
    
    label backpack:
        v "Finally, I pack everything into my backpack."
        v "It's a struggle every morning shoving everything in there."
        v "A binder of long-obsolete worksheets, a handful of stray pencils, a laptop with more miscellaneous papers inside..."
        v "Not to mention my lunch and water bottle."
        v "I return to my room to grab my shoulder bag, plopping my phone in while I'm at it."
        v "Then we're off."
        mom "\"Have fun at school, sweetie!\""
        v "\"Mmhm...!\""
        v "Quite honestly, I'm just hoping to make it through the day in one piece."

        ## Resizing backgrounds using an ATL statement, equivalent to Python's transform()
        scene car:
            zoom 0.8


        v "The car ride to school is relatively uneventful. The radio provides background noise as I stare listlessly out the window."
        v "Maybe I should entertain myself?"

        menu carchoice:
            "Take my phone out.":
                $ Physical += 1
                $ Social -= 1
                call minlimit from _call_minlimit_6
                show screen multinotify(["Physical stress +1: " + str(Physical), "Social stress -1: " + str(Social)])
                v "I scroll mindlessly through social media."
                v "I guess now is a good time to start replying to all the messages I was ignoring yesterday."
                v "As the kind and sociable friend that I am, I reply to all my texts curtly and leave little room for extended conversation."
                v "Then again, I don't think it's unreasonable to not want to talk so much in the morning."
                v "I'm going to be seeing everyone at school, anyway."
                if sick:
                    $ Physical += 2
                    $renpy.notify("Physical stress +2: " + str(Physical))
                    v "{i}Now I'm carsick...{/i}"
            "Listen to the radio.":
                $ Mental += 2
                $renpy.notify("Mental stress +2: " + str(Mental))
                v "I don't know why I chose to do that."
                v "Honestly, I hate listening to the radio. Their voices are always so grating, and even on the off-chance that I can tolerate them, they're always talking about something I don't want to listen to."
                "Radio" "\"...So that's why you should wear socks with at least three holes in them!\""
                v "...?"
                v "You know what, I have no idea what they're talking about, but good for them(?)"
            "Do nothing.":
                v "...Then again, maybe not."
                v "I get carsick easily, so I should just keep staring out the window."
        v "In my head, I bemoan the fact that the car ride is just long enough to force me to wake up early, but not long enough for me to fall back asleep."
        v "It would be nice to be born with the skill of passing out right away..."
        v "But I guess I'll have to tolerate the rest of the trip until we're there."
        
        scene kss with dissolve

        v "Finally, we arrive."

        if not late: 
            v "I've still got a bit of time to spare."
            v "Should I head to class right away, or...?"
            menu:
                "I'll go sit in the atrium with friends.":
                    $ Social -= 2
                    call minlimit from _call_minlimit_7
                    $renpy.notify("Social stress -2: " + str(Social))
                    scene atrium:
                        zoom 1.6
                    v "Since I've got the time, I might as well say hi to my friends."
                    v "We greet each other as they make room for me to take a seat."
                    v "It's still too early for me to be a functioning member of society, though, so I end up pulling out my phone."
                    v "Together, we all sit there for a while, staring at our devices and occasionally sharing an entertaining post."
                    v "It's not too bad, but in the back of my head I'm constantly making note of every minute that passes."
                    v "Eventually, the dreaded bell rings."
                    v "Some of us go our separate ways, while others follow me to the science classroom."
                    jump scienceclass

                "I'll go to class.":
                    $ Social += 1
                    $ Mental -= 1
                    call minlimit from _call_minlimit_8
                    show screen multinotify(["Social stress +1: " + str(Social), "Mental stress -1: " + str(Mental)])

                    v "I'm too tired to talk to people right now."
                    v "I'll wait until I'm awake enough to behave like an actual person to talk to my friends."
                    v "For now, I head to class, switching my shoes at my locker."
                    scene classroom1
                    v "Lugging my backpack with me into class, I give the teacher a civil greeting."
                    v "\"Good morning...\""
                    v "I yawn in the middle of my greeting, which Mr. Cross light-heartedly pokes fun at me for."
                    v "Whenever I see him in the morning, he's always lugging things around from place to place."
                    v "Wonder where he gets the energy from."
                    v "I drop off my backpack somewhere near my desk before attempting to pick up three chairs at once from an already precarious-looking stack."
                    v "As long as it doesn't fall on me, it doesn't matter, right?"
                    v "With some luck, I manage to get back to my desk and put the chairs down in place."
                    v "I greet the classmates who are already at their seats, studying for the upcoming exam."
                    v "Very diligent of them. I should follow their example."
                    v "...I mean, I won't, but I definitely should."
                    v "Instead, I mindlessly scroll on my phone until the bell rings and everyone comes pouring in."

                
                "I'll go find Mr. Delva.":
                    $ techflags += 1
                    v "I am suddenly consumed with an all-powerful urge to track down my tech class teacher."
                    v "I should talk to him about my culminating project..."
                    v "It's getting pretty stressful trying to balance my extracurriculars with studying for exams along with this final project."
                    v "Maybe I should ask him for an extension."
                    v "However, after a while of searching, there's still no Mr. Delva to be found."
                    v "I guess I'll just have to cross my fingers and pray for a good mark."
                    v "{i}Have pity on me, Mr. Delva.{/i}"
                    v "The bell rings, putting an end to my unfruitful search, and I head to science class."
                    jump scienceclass
                    
        else:
            v "I rush through the halls, barely making it to my first class before the bell rings."
            scene classroom1
            v "Everyone is already in their seats. I note that someone has already gotten me a chair, and I mutter a quiet thanks."
    
    label scienceclass:
        scene classroom1
        v "Everyone sits patiently through the announcements."
        v "I don't particularly care to listen."
        ## {a} allows for interactive links to be included in text.
        ## Applications of this can also be seen in the About page (options.rpy --> gui.about)
        v "All the announcements end up on the {a=https://discord.gg/DAcWnXA7b9}{u}KSS Directory Discord server{/a}{/u}, so I'll just check there later."
        v "Nearing the end of the announcements, the class gets just slightly loud enough that I don't catch the joke of the day."
        v "Is it worth asking someone...?"
        menu joke:
            "Ask a classmate what the joke of the day was.":
                v "I tap on the shoulder of the girl sitting in front of me."
                v "\"Hey, what was the joke? I couldn't hear it.\""
                ## {p} Splits the dialogue so you have to click again to see the joke even though it's in the same textbox
                "Ella" "\"What do you call a psychic little person who has escaped from prison? {p} A small medium at large.\""
                if Mental > 20:
                    $ Mental += -2
                    $renpy.notify("Mental stress -2: " + str(Mental))
                    call minlimit from _call_minlimit_9
                    v "\"...Heh.\""
                    v "You know what, that was pretty stupid."
                    v "Stupid enough to be funny."
                    ## xalign 0.0 aligns the object with the left side of the frame, linear is the amount of time it takes for the movement to happen
                    show cross erased:
                        linear 0.5 xalign 0.0
                    c "\"Whaaaaat? That's so lame!\""
                    hide cross erased with dissolve
                    v "...Mr. Cross might disagree."
                    v "But he's wrong. That was a pretty awesome joke."
                    v "Good enough to make a bad day just a little better."
                else: 
                    $ Mental -= 1
                    call minlimit from _call_minlimit_10 
                    $renpy.notify("Mental stress -1: " + str(Mental))
                    v "..."
                    v "..."
                    v "...?"
                    v "...!"
                    v "Ohhhh!!"
                    v "That was pretty funny."
                    v "Not exactly a knee-slapper, but punny enough for me."

            "What? Who cares?":
                v "I guess I'm just in a bad mood today."
                v "Or every day, really, when I have to be at school."
                v "I have lost all sense of joyful whimsy. No longer do I care about such trivial things like jokes."
        
        v "Soon after, everything is set for class to start."
        v "Today is a pretty boring day for science class."
        v "Some video-watching, some textbook-reading..."
        v "I just hope Mr. Cross doesn't call on me to answer a question."
        v "He's usually pretty nice about letting students answer only when they want to, but..."
        if sick: 
            v "I feel so sick, I really want to minimize every second of time I have to spend speaking in front of the class."
        else:
            v "The people around me tend to participate in class a lot, so I might end up grouped up with them."
        show cross erased 
        
        c "\"So, who knows the answer to the question?\""
        "..."
        "..."
        "..."
        v "Ah, times like this come up every once in a while."
        v "Questions that are either too vaguely phrased to be answered, or just straight up too tricky for anyone to know."
        v "No one wants to be the one to put their hand up and take the risk."
        v "There's some mumbling around me—classmates who think they might know the answer but aren't confident enough to try..."
        v "But if we wait it out long enough, I know Mr. Cross will just tell us the answer."
        c "\"Come on now!\""
        c "\"Guys, if no one answers, I'm going to pick someone randomly to speak...\""
        v "!!"
        v "Or not, I guess...!"
        v "That's not good. I was too busy zoning out to even hear what the question was."
        v "There's a few people around me who seem to share the same sentiment as me."
        v "{i}Please don't pick me, please don't pick me..."
        v "There's got to be someone willing to take one for the team and guess, right?"
        v "Alas, nothing but silence fills the room."

        ## I realize this might've worked better as a coinflip from 1 to 2 
        ## and had my conditional statement revamped to "if conflip == 1"/"else" 
        ## but I wanted an excuse to use modulus :)
        $ coinflip = renpy.random.randint(2,3)
        if coinflip%2 == 0:
            c "\"Valerie! You look like you know the answer! Why don't you give us a guess?\""
            v "!!" with vpunch
            v "Uh-oh..."
            v "Forget knowing the answer, I don't even know the question!"
            v "\"Uhhh...\""
            v "\"Could you repeat the question?\""
            v "Mr. Cross chuckles knowingly, curse him. I bet he knew I wasn't listening."
            v "Come on. I'm usually a decent student! It was just this once!"
            c "\"If an object is placed between the focus and the centre of curvature of a concave mirror, what will its image look like?\""
            show cross erased:
                linear 0.5 xalign 0.05
            menu physics:
                c "{cps=0}\"If an object is placed between the focus and the centre of curvature of a concave mirror, what will its image look like?\""

                "The image will be bigger and upright.":
                    if not physicsq:
                        $ Social += 3
                        $ Mental += 3
                        show screen multinotify(["Social stress +3: " + str(Social), "Mental stress +3: " + str(Mental)])
                    show cross erased:
                        linear 1.0 xalign 0.5
                    c "\"Mmm... close, but not quite...\""
                    c "\"Can anyone else tell me the answer?\""
                    c "\"Sofia? How about you?\""
                    "Sofia" "\"The image will be larger and inverted.\""
                    v "I'd like to perish in my seat, if I could."
                    v "It's probably not that big of a deal, but that was pretty embarrassing."
                
                "The image will be bigger and inverted.":
                    $ Social -= 3
                    $ Mental -= 3
                    call minlimit from _call_minlimit_11
                    show cross erased:
                        linear 1.0 xalign 0.5
                    c "\"You got it!\""
                    show screen multinotify(["Social stress -3: " + str(Social), "Mental stress -3: " + str(Mental)])
                    c "\"See, guys, that wasn't that hard!\""
                    v "Speak for yourself, Mr. Cross."
                    v "My anxiety just spiked to an all-time high."

                "The image will be smaller and upright.":
                    if not physicsq:
                        $ Social += 4
                        $ Mental += 4
                        show screen multinotify(["Social stress +4: " + str(Social), "Mental stress +4: " + str(Mental)])
                    v "I can see my classmates giving each other confused glances all around me."
                    v "Wow, I guess I was really wrong."
                    v "Even Mr. Cross is looking at me like I'm a fascinating specimen with limited intelligent capacity."
                    v "Whoops."
                    show cross erased:
                        linear 1.0 xalign 0.5
                
                    c "\"Well...\""
                    c "\"You'd be right if it was opposite day!\""
                    c "\"The image will be larger and inverted, actually.\""
                    c "\"'Good' guess, though...?\""
                    v "Well, at least he's not ragging on me too much."
                    v "I just said the first thing that came to mind, anyway."

                "The image will be smaller and inverted.":
                    if not physicsq:
                        $ Social += 3
                        $ Mental += 3
                        show screen multinotify(["Social stress +3: " + str(Social), "Mental stress +3: " + str(Mental)])
                    show cross erased at center
                    c "\"Mmm... close, but not quite...\""
                    c "\"Can anyone else tell me the answer?\""
                    c "\"Sofia? How about you?\""
                    "Sofia" "\"The image will be larger and inverted.\""
                    v "I'd like to perish in my seat, if I could."
                    v "It's probably not that big of a deal, but that was pretty embarrassing."

                "I don't know...?" if not physicsq:
                    $ Social += 1
                    $ Mental += 1
                    show screen multinotify(["Social stress +1: " + str(Social), "Mental stress +1: " + str(Mental)])
                    $ physicsq = True
                    c "\"Well, why don't you give us a guess, anyway?\""
                    v "Darn. I was hoping he would take pity on me, but I guess I gotta give this a shot."
                    jump physics

        else:
            c "\"Sofia! You look like you know the answer! Why don't you give us a guess?\""
            $ Mental -= 2
            call minlimit from _call_minlimit_12
            v "Phew..."
            $renpy.notify("Mental stress -2: " + str(Mental))
            v "Glad it was someone else who was thrown under the bus."
            v "I bet in some alternate universe, I had to answer the question."
            v "It's a good thing it looks like Sofia knows what she's doing."
            "Sofia" "\"The image of the reflected object will be larger and inverted.\""
            c "\"Excellent!\""
            c "\"See, that wasn't that hard, was it?\""

        hide cross erased
        v "The rest of the class passes fairly uneventfully."
        v "I take notes in my notebook, making sure to pay the utmost attention in case I'm caught off guard again."

        if sick:

            $ coinflip = renpy.random.randint(1,3)
            if coinflip % 3 == 0:
                $ Physical += 3
                $ headache = True
                v "Even so, I think I'm starting to develop a headache."
                v "Looking down on my notes is starting to make my head spin."
                v "And my stomach is starting to gurgle in disagreement with the breakfast I had forced down earlier."
                $renpy.notify("Physical stress +3: " + str(Physical))
                v "Ugh... I gotta be strong..."
                v "Class will be over soon."
            elif coinflip % 3 == 1:
                $ Physical += 1
                v "Even so, I still feel pretty awfully sick."
                $renpy.notify("Physical stress +1: " + str(Physical))
                v "Accursed winter weather..."
                v "I put my coat on a little tighter, hoping to preserve what warmth I still have."
            else: 
                $ Physical -= 1
                call minlimit from _call_minlimit_13
                v "At least I'm starting to feel a bit better, in terms of the stuffy nose and dry throat."
                $renpy.notify("Physical stress -1: " + str(Physical))
                v "I grab a drink of water, soothing my throat further."
                v "Seems like today is going better than usual in terms of recovering from my morning allergies."

    label historyclass:
        v "Finally, the bell rings to signal the end of class."
        v "Electing to not look at the whiteboard with tonight's homework scrawled on it, I head up the stairs to history class."
        scene classroom2:
            zoom 0.4
        v "I take my seat, noting that the desks have moved slightly since yesterday."
        v "\"These desks are so stupid...\""
        v "I don't know whose genius idea it was to make these absurd flower-petal shaped, asymmetric desks..."
        v "But I hope they're in severe pain right now."
        v "They're a pain to sit behind, they're a pain to move, they're a pain to put back in their original orientation..."
        v "They better be cheaper than the regular rectangular desks, because otherwise I can think of no rational reason why our school would choose to torture us with these desk models instead."
        
        ## Lots of RNG involved in events of the game.
        if sick:
            if headache:

                $ coinflip = renpy.random.randint(1,3)
                if coinflip % 2 == 0:
                    $ Physical += 2
                    $renpy.notify("Physical stress +2: " + str(Physical))
                    v "Great, the headache's only gotten worse after that rant..."
                    v "I fish around my backpack looking for my waterbottle."
                    v "I'm not looking forward to having history while I'm already in this much pain."
                    v "A headache, a runny nose, a tummyache, {i}and{/i} sweaty palms..."
                    v "I can only hope it all subsides soon."
                elif coinflip == 1:
                    v "Hnngh..."
                    v "A sudden wave of nausea strikes me."
                    v "My pathetic immune system is clearly not fighting well enough for me."
                    v "Even though this happens pretty often, it's not usually this bad."
                    v "Maybe I should throw in the white flag..."
                    menu callhome:
                        "Call home.":
                            v "Screw it. I'm not going to last the whole school day like this."
                            v "It's not like I'll be able to focus on class when my vision is blurring from my eyes watering."
                            $renpy.notify("Valerie: dad i dont feel good can you pick me up")
                            v "I shoot my dad a quick text, then walk over discreetly to Mr. Wordley's desk."
                
                            v "\"Excuse me...\""
                            w "\"Yes?\""
                            v "\"I'm... not feeling great right now. I've messaged my parents to come pick me up, so could I go?\""
                            w "\"Oh yeah, sure. Just make sure to catch up on the work on the Minds Online.\""
                            v "\"Alright, thanks!\""
                            
                            v "Phew. I head down to the atrium stairs, waiting for a reply from my father."
                            $renpy.notify("Dad: ok coming in 20 mins")
                            $renpy.pause(1.0)
                            v "Wearily, I let my head rest against the wall as I scroll on my phone."
                            v "Soon, my dad comes to pick me up."
                            scene car:
                                zoom 0.8
                            v "At home, I can finally rest and recover."
                            v "It's okay to take a day off when I need it..."
                            scene bedroom dim
                            
                            v "I'm gonna take a nap for now, though."
                            v "Goodnight..."
                            scene black with fade
                            v "..."
                            v "..."
                            v "..."
                            centered "(A few hours later:)"
                            v "!!"
                            scene bedroom dim with fade
                            v "When I wake up, the first thing I notice is that I don't feel nearly as awful anymore."
                            v "The second thing I realize is that it's- {p} {size=+20}\"3:30?!\""
                            v "\"Haha...\""
                            v "I guess I must have been very, very, tired."
                            v "That nap did good things to me, though."
                            v "I feel rejuvenated!"
                            $ Physical -= 10
                            call minlimit from _call_minlimit_14
                            $renpy.notify("Physical stress -10: " + str(Physical))
                            v "Well, now I've got to be productive."
                            v "If I'm awake, alive, and not feeling as awful..."
                            v "Then I should get studying!"
                            v "But..."
                            jump funtimes
                        "Stay at school.":
                            $ Physical += 10
                            v "Nooo..."
                            v "I have to stay strong..."
                            $renpy.notify("Physical stress +10: " + str(Physical))
                            v "Gotta power through today!!!"
                            v "I'll be suffering all the while, but at least I won't miss any work in this last week of school before exams..."
                else:
                    v "The headache is still there, but it's gotten a little better."
                    v "I hope history class treats me a little better than science."
                    v "If I have to deal with this all day, I think I might actually cry."
            else:
                v "Well, I'm just not having a good time now, am I."

        v "For all my grumbling, I'm almost happy to have class start."
        v "At least it'll give me something else to focus on."
        w "\"Alright guys, look up at the screen and put your phones away.\""
        w "\"Today we'll be picking up where we left off on American-Canadian relations.\""
        show slideshow with dissolve
        v "Mr. Wordley has a slideshow presentation open."
        v "I watch absent-mindedly as he clicks through slides, summing up the text and images before moving on to the next slide."
        v "Despite what just happened in science class, I find myself zoning out again."
        v "Thankfully, this time I don't have to worry about being called out for it."
        hide slideshow with dissolve
        v "We make it through the presentation, then he gives us twenty minutes to work on the discussion question posted on Minds Online."
        v "Honestly, I don't want to do it, but it's not hard to write up something random that sounds smart enough to fly under the radar."
        v "I'll finish it up quickly, then spend the rest of class time daydreaming."
        v "\"Let's see... the discussion prompt is 'the pros and cons of having America as an ally'.\""
        v "Alright, that's not too hard."
        v "Given everything we've talked about in class..."

        $ historyanswer = renpy.input("What are the pros and cons of being allied with the United States?",length=100, multiline=True)
        $ historyanswer = historyanswer.strip()
        w "\"Let's look at some of your answers, huh?\""
        w "\"Valerie...\""
        ## Punishes people who skip ahead without inputting anything :D
        if len(historyanswer) <= 3:
            w "\"Stay on task! It's not that hard to write an actual answer to the discussion prompt!\""
            $ Mental += 1
            $ Social += 1
            show screen multinotify(["Mental stress +1: " + str(Mental), "Social stress +1: " + str(Social)])
            v "Whoops."
            v "Embarrassed, I type an actual response to the discussion prompt."
            v "Class ends shortly after, and I soon forget about my publicized shame."
        else:
        
            w "\"'[historyanswer]...'\""
            w "\"Interesting point of view. I'll write a comment under your post.\""
            python:
                if "support" or "military" or "close" or "allies" or "war" or "trade" in historyanswer:
                    Social += -1
                    renpy.notify("Social stress -1:" + str(Social))
            w "\"Remember to comment under at least 2 other peoples' posts, everyone!\""
            v "...I mean..."
            v "He says that, but there's only five minutes left of class, and it's not like he'll check."
            v "Still, just in case, I write a few short comments under my friends' posts."

    label lunch:
        v "Finally, the lunch bell rings."
        v "It's like taking a breath of fresh air as I step outside of the classroom."
        v "Now I've got the freedom to choose what I want to do."
        v "What should I do during lunch?"
        menu lunchchoice:
            v "{cps=0}What should I do during lunch?"

            "Eat in the atrium.":
                jump atriumlunch
            "Go to science club.":
                jump scienceclub
            "Go to math club.":
                jump mathclub
            "Take a nap." if sick or Mental > 20:
                jump nap
            "Work on my tech project.":
                jump tech   

    label atriumlunch:
        $ Physical -= 3
        call minlimit from _call_minlimit_15
        $renpy.notify("Physical stress -3: " + str(Physical))
        v "Yeah, I think I'll skip on my clubs today..."
        v "It's not like I can eat in the science lab, and I always forget to eat during math club."
        if sick:
            v "I have to get something in my stomach, anyway."
            v "Gotta stay energized if I want to keep making it through the day..."
        elif late:
            v "I barely got to eat anything for breakfast, so now is the time to compensate!"
        scene atrium:
            zoom 1.6

        v "I'm the first to arrive in the atrium out of all my friends who eat there."
        v "I've always thought that that was weird. I mean, history class is on the third floor!"
        v "But it takes everyone upwards of five minutes to get here every day."
        v "Then again, maybe they have things to do other than come sit down on the crusty atrium steps to eat lunch..."
        v "Sad thought."
        v "Well, socializing in the halls right after class is pretty terrible in my opinion anyway."
        v "So many people..."
        v "Plus you have a high chance of accidentally bumping into someone at the stairwell while you're turning that corner!"
        v "Terrible design, really."
        v "Much like the atrium stairs. I mean, what even is going on there?"
        v "Your options are either to take giant steps or itty-bitty baby steps to get to the second floor."
        v "This is a hill I'm very willing to die on."
        v "I know I have friends who are willing to do so as well."
        v "Ah, speak of the devil..."
        v "\"Matthew, don't these stairs suck?\""
        v "I'm calling out to Matthew, who I can see taking pained steps up from the first floor to get to the step that I'm sitting on."
        v "Odd way to start a conversation, but I am nothing if not spontaneous."
        $ coinflip = renpy.random.randint(1,2)
        if coinflip == 1:
            "Matthew" "\"(Generic Matthew Rant)\""
        else:
            "Matthew" "\"Well, to begin, the actual stairs are too short for anyone to feasibly walk on. They're clearly not built for any human walking in mind, because they're way too easy to fall down; the steps are too small to walk up at a comfortable pace but also too big to skip steps without it being a huge annoyance too. They added the black paint for what feels like no reason, and the big steps don't really add anything more than a bunch of discomfort to an area that was already terrible to be around. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\""
        v "So true!"
        v "Anyway, everyone congregates around me eventually."
        v "I'm a little more awake now, so I can converse comfortably with everyone."
        if Social < 20:
            v "Speaking of which..."
            menu convochoices:
                "\"How is everyone's English project going?\"":
                    v "I know I'm the one asking, but it's really just to see all the English-class-havers grow flustered."
                    v "I'm told that they have both a personal essay to write {i}and{/i} an exam."
                    v "Luckily, my third period class is occupied with the illustrious Digital Technology and Innovations in the Changing World class, so I'm free to make fun of them all I want."
                    v "Until next semester, but that's not for, like, a week."
                    "Elizabeth" "\"I hate you.\""
                    "Cecilia" "\"Shut up.\""
                    "Tasnia" "\"Actually die.\""
                    v "Yum."
                    v "I thrive on their despair."
                "\"How is Math treating everyone?\"":
                    v "Apparently the Math class got a new teacher in the middle of the semester."
                    v "Rough for them, but couldn't be me."
                    v "I heard they had a test during second period, and from the weary faces everyone is wearing, it was not a very good one."
                    "Ethan" "*shrug*"
                    "Sofia" "\"Haha... I mean, it was okay...\""
                    "Jessie" "\"Terrible. Horrible. I actually hated that.\""
                    v "Glad I didn't have to do it, then."
                    v "At least history class is tolerable!"
                "\"I love tech class.\"":
                    $ techflags += 1
                    v "Yeah!!! Tech class!! Awesome!!"
                    v "Some people shoot me strange looks, but they simply wouldn't get it."
                    v "It's super awesome how I decided to scrap my final project two times over and ended up having to rewrite all of my code of the course of one weekend."
                    v "It's also really cool how I decided to focus on the graphics until I realized too late that I was only one-third finished the actual dialogue."
                    v "I'm really having the time of my life here."
                    v "I'd like to believe if Mr. Delva were here right now, he would be giving me his blessing."
                    v "After all, you couldn't find a more dedicated student than me to my culminating project!!!"
                    "Matthew" "\"Are you... like... feeling alright?\""
                    v "\"Oh yeah, I'm fine. Don't worry about it.\""
                    v "All is well. I've ascended to a higher spiritual plane."
                    v "The material world means nothing to me. A complete program is no more than an illusion. The real final project was the friends we made along the way."
                    "Sofia" "..."
                    "Ethan" "..."
                    "Eileen" "..."
                    v "\"Yay!!\""
        elif techflags == 1:
            $ techflags += 1
            v "Doesn't mean I will, though."
            v "Why spend time talking when I could be coding?"
            v "Why spend time doing anything at all when I could be coding?"
            v "Why am I here? Where is my computer??" 
            with hpunch
            v "Someone just shook me very hard."
            "Jessie" "\"Val, I'm glad you're having a good time right now, but if you could stop muttering cultish chants about your code project...\""
            v "Ah. Oops."
            v "I return to my lunch in a perfectly healthy state of mind."
        else:
            v "Doesn't mean I will, though."
            v "I've got enough on my plate as is."
            v "Might as well use this time as a much-needed break from everything school-related."
        v "Anyway, the time slips through my fingers all too easily."
        v "Soon, lunch comes to an end, and we all go to our third period class."
        if techflags == 2:
            v "Now to my favourite class of the day...!"
        v "To tech class I'll go."
        jump techclass

    
    label scienceclub:
        $ Physical += 2
        $ Social -= 3
        call minlimit from _call_minlimit_16
        show screen multinotify(["Social stress -3: " + str(Social), "Physical stress +2: " + str(Physical)])
        v "Mhmm..."
        v "As part of the newly-formed Science Club exec team, it's my obligation to attend every meeting!"
        v "I would never ever dream of skipping out on it."
        v "I do have to check my phone to remember which room we're having our meeting in..."
        v "But that's all par for the course, and anyway I get there eventually."
        scene classroom1
        v "There, I greet my favourite Science Club president..."
        menu importantchoice:
            "Siya, of course!":
                v "\"Hi Siya!!!\""
                v "\"You are so cool and awesome!!!\""
                v "\"I love you so much.\""
                s "\"That's crazy.\""
                $renpy.notify("Siya's affection points +1")
                v "She's so cool like that."
            "Arzoi, naturally!":
                v "\"Hi Arzoi!!!\""
                v "\"You are so cool and awesome!!!\""
                v "\"I love you so much.\""
                $ coinflip = renpy.random.randint(1,2)
                if coinflip == 1:
                    "Arzoi" "\"Hey girl!\""
                else:
                    "Arzoi" "\"Go piss girl!\""
                $renpy.notify("Arzoi's affection points +1")
                v "We're so close like that."
        v "I exchange greetings with everyone else too, of course."
        v "We might be a newly established club, but that just means that we're all very close with each other."
        v "Today's meeting is, as determined by popular vote, another GeoGuessr meeting!"
        v "I've never been very good at it, but I know many of our members are very, very competitive about it."
        v "I'm content to be Siya's sidekick again, like I have been every other time."
        v "Granted, it might be more appropriate to call myself her saboteur, considering how many times I've misled her from her original guess."
        v "It might be easier this time, though! For our warm-up session, we're just going over famous cities, so it can't be that hard."
        show geoguessr paris with fade
        window hide
        $renpy.pause
        window show
        menu paris:
            "Hmm, this looks like it's in..."

            "Asia":
                v "Yeah, sounds about right."
                v "\"How about Asia?\""
                s "???"
                s "\"Okay Valerie, I trust you...\""
                gg "Wrong! Paris!"

            "North America":
                v "Yeah, sounds about right."
                v "\"How about North America?\""
                s "???"
                s "\"Okay Valerie, I trust you...\""
                gg "Wrong! Paris!"

            "South America":
                v "Yeah, sounds about right."
                v "\"How about South America?\""
                s "???"
                s "\"Okay Valerie, I trust you...\""
                gg "Wrong! Paris!"

            "Australia":
                v "Yeah, sounds about right."
                v "\"How about Australia?\""
                s "???"
                s "\"Okay Valerie, I trust you...\""
                gg "Wrong! Paris!"
            
            "Europe":
                v "Yeah, sounds about right."
                v "\"How about Europe?\""
                s "Hmm..."
                s "\"Okay Valerie, I trust you...\""
                s "\"Where in Europe?\""
                $renpy.pause
                menu paris2:
                    "Italy":
                        gg "Wrong! Paris!"
                        $ geopoints += 1       
                    "Germany":
                        gg "Wrong! Paris!"
                        $ geopoints += 1
                    "United Kingdom":
                        gg "Wrong! Paris!"
                        $ geopoints += 1
                    "France":
                        s "\"Sounds reasonable...\""
                        s "\"Where in France?\""
                        $renpy.pause
                        menu paris3:
                            "Paris":
                                gg "Good job! You were right!"
                                s "Yay! Good job, Valerie!"
                                $ geopoints += 5
                            "Marseille":
                                gg "Wrong! Paris!"
                                $ geopoints += 3
                            "Lyon":
                                gg "Wrong! Paris!"
                                $ geopoints +=3
                            "Toulouse":
                                gg "Wrong! Paris!"
                                $ geopoints += 3
            "Africa":
                v "Yeah, sounds about right."
                v "\"How about Africa?\""
                s "???"
                s "\"Okay Valerie, I trust you...\""
                gg "Wrong! Paris!"

        if geopoints == 5:
            v "You know what, not a bad first round from me!!"
            v "Maybe I'm not as bad as I thought I would be."
            v "It looks like Siya feels the same. Maybe she's starting to trust me again after I failed her royally at our last meeting..."
        elif 1 <= geopoints <= 3:
            v "Uhh... could've been worse?"
            v "At least I didn't guess the wrong continent!"
            v "Next up..."
        else: 
            v "Oops."
            s "\"Valerie! I trusted you!\""
            v "..."
            v "\"Teehee?\""
            v "Ahem. Next round!!"

        label losangeles:
            show geoguessr los angeles with fade
            window hide
            $renpy.pause
            window show
            menu losang:
                "Hmm, this looks like it's in..."

                "Asia":
                    v "Yeah, sounds about right."
                    v "\"How about Asia?\""
                    s "???"
                    if geopoints == 5:
                        s "\"Okay Valerie...\""
                    else:
                        s "\"Sure...\""
                    gg "Wrong! Los Angeles!"

                "North America":
                    v "Yeah, sounds about right."
                    v "\"How about North America?\""
                    s "\"Okay Valerie, I trust you...\""
                    s "\"Where in North America?\""
                    $renpy.pause
                    menu losang2:
                        "Canada":
                            $ geopoints += 1
                            gg "Wrong! Los Angeles!"
                        "United States":
                            s "\"Hmm, okay.\""
                            s "\"Where in the United States?\""
                            $renpy.pause
                            menu losang3:
                                "New York":
                                    $ geopoints += 3
                                    gg "Wrong! Los Angeles!"

                                "Los Angeles":
                                    $ geopoints += 5
                                    gg "Good job! You were right!"
                                    if geopoints == 10:
                                        s "\"Wow Valerie, you've really improved since last week!\""
                                        s "\"I can almost forgive you for how you've wronged me!\""
                                    else:
                                        s "\"Congrats us! Maybe we'll place 2nd from last place this time!\""    
                                "Chicago":
                                    $ geopoints += 3
                                    gg "Wrong! Los Angeles!"
                        "Mexico":
                            $ geopoints += 1
                            gg "Wrong! Los Angeles!"

                "South America":
                    v "Yeah, sounds about right."
                    v "\"How about South America?\""
                    s "???"
                    if geopoints == 5:
                        s "\"Okay Valerie...\""
                    else:
                        s "\"Sure...\""
                    gg "Wrong! Los Angeles!"

                "Australia":
                    v "Yeah, sounds about right."
                    v "\"How about Australia?\""
                    s "???"
                    if geopoints == 5:
                        s "\"Okay Valerie...\""
                    else:
                        s "\"Sure...\""
                    gg "Wrong! Los Angeles!"
                
                "Europe":
                    v "Yeah, sounds about right."
                    v "\"How about Europe?\""
                    s "Hmm..."
                    if geopoints == 5:
                        s "\"Okay Valerie...\""
                    else:
                        s "\"Sure...\""
                    gg "Wrong! Los Angeles!"
                
                "Africa":
                    v "Yeah, sounds about right."
                    v "\"How about Africa?\""
                    s "???"
                    if geopoints == 5:
                        s "\"Okay Valerie...\""
                    else:
                        s "\"Sure...\""
                    gg "Wrong! Paris!"

        label tokyo:
            if geopoints == 10:
                v "For once, we're in the running for the lead!"
                v "It all comes down to this last one."
                v "Siya and I look at each other with determination in our eyes."
                v "This will forever decide the fate of our friendship."
            elif 1 <= geopoints <= 8:
                v "We've made some mistakes, but I guess we've done worse..."
                v "We're on the last question, so maybe if everyone else screws up we still have a chance."
                v "I take a deep breath, waiting for the round to start."
            else:
                v "It's so doomed."
                v "At most we can hope for second last place..."
                v "Or maybe not. I think we're the only team with 0 points."
                v "I feel like I should get an award for this."
                $renpy.notify("Achievement unlocked: GeoGuessr Failure")
                v "Hey! What was that?!"
                v "I'm no failure!! Trust me, I'll get this last round perfect."
            show geoguessr tokyo with fade
            window hide
            $renpy.pause
            window show
            menu tokyo1:
                "Hmm, this looks like it's in..."

                "Asia":
                    v "Yeah, sounds about right."
                    v "\"How about Asia?\""
                    if geopoints == 10:
                        s "\"Yes Valerie!!!! Let's do this!!\""
                    elif geopoints > 0:
                        s "\"Yeah, okay...\""
                    else: 
                        s "..."
                    s "\"Where in Asia?\""
                    $renpy.pause
                    menu tokyo2:
                        "{cps=0}It looks like..."

                        "China":
                            gg "Wrong! Tokyo!"
                            if geopoints > 0:
                                $ geopoints +=1
                            else:
                                s "\"Hey! Why did you click that?!\""
                                s "\"It definitely wasn't going to be there...\""
                                s "\"I'm never teaming up with you again.\""
                        
                        "Japan":
                            s "!!"
                            s "\"Okay, I think you're right about that...\""
                            s "\"But where in Japan?\""
                            $renpy.pause
                            menu tokyo3:
                                "Kyoto":
                                    gg "Wrong! Tokyo!"
                                    $ geopoints += 3

                                "Osaka":
                                    gg "Wrong! Tokyo!"
                                    $ geopoints += 3

                                "Tokyo":
                                    gg "Good job! You were right!"
                                    $ geopoints += 5
                                    if geopoints == 5:
                                        s "\"You know what, I'll forgive you for everything else you've done today!\""
                                        s "\"At least we got one thing right.\""
                                    if geopoints == 15:
                                        $renpy.notify("Achievement unlocked: GeoGuessr Master")
                                        v "\"YAY!\"" with hpunch
                                        "Rest of Science Club" "!!"
                                        v "Siya and I high five each other, proud of our accomplishment."
                                        v "It seems like just a week ago, we were at each others' throats, but we've finally put aside our differences and achieved the most important goal:"
                                        v "Beating everyone else at GeoGuessr!"
                                        v "Albert, Ethan, Matthew, Arzoi, Mary..."
                                        v "They fought valiantly, but none could triumph over the power of true friendship!"
                                        v "I could die happy now."
                                        v "But I don't need to, 'cause we won at GeoGuessr!"
                                    if 15 > geopoints > 5:
                                        v "We fought valiantly, but ultimately our earlier failures led us to be unable to take the crown."
                                        v "Still, Siya and I accept our loss gracefully."
                                        v "Maybe next week we'll get it."

                                "Okinawa":
                                    gg "Wrong! Tokyo!"
                                    $ geopoints += 3

                        "India":
                            gg "Wrong! Tokyo!"
                            if geopoints > 0:
                                $ geopoints +=1
                            else:
                                s "\"Hey! Why did you click that?!\""
                                s "\"It definitely wasn't going to be there...\""
                                s "\"I'm never teaming up with you again.\""

                        "Thailand":
                            gg "Wrong! Tokyo!"
                            if geopoints > 0:
                                $ geopoints +=1
                            else:
                                s "\"Hey! Why did you click that?!\""
                                s "\"It definitely wasn't going to be there...\""
                                s "\"I'm never teaming up with you again.\""

                        "South Korea":
                            gg "Wrong! Tokyo!"
                            if geopoints > 0:
                                $ geopoints +=1
                            else:
                                s "\"Hey! Why did you click that?!\""
                                s "\"It definitely wasn't going to be there...\""
                                s "\"I'm never teaming up with you again.\""

                        "Indonesia":
                            gg "Wrong! Tokyo!"
                            if geopoints > 0:
                                $ geopoints +=1
                            else:
                                s "\"Hey! Why did you click that?!\""
                                s "\"It definitely wasn't going to be there...\""
                                s "\"I'm never teaming up with you again.\""

                "North America":
                    v "Yeah, sounds about right."
                    v "\"How about North America?\""
                    s "???"
                    if geopoints == 10:
                        s "\"This sounds stupid, but I'll trust you.\""
                        gg "Wrong! Tokyo!"
                    elif geopoints > 0:
                        s "\"Sure...\""
                        gg "Wrong! Tokyo!"
                    else: 
                        s "\"You know what, I'm not listening to you anymore.\""
                        s "\"This looks like Asia to me.\""
                        jump tokyo2
                    
                "South America":
                    v "Yeah, sounds about right."
                    v "\"How about South America?\""
                    s "???"
                    if geopoints == 10:
                        s "\"This sounds stupid, but I'll trust you.\""
                        gg "Wrong! Tokyo!"
                    elif geopoints > 0:
                        s "\"Sure...\""
                        gg "Wrong! Tokyo!"
                    else: 
                        s "\"You know what, I'm not listening to you anymore.\""
                        s "\"This looks like Asia to me.\""
                        jump tokyo2

                "Australia":
                    v "Yeah, sounds about right."
                    v "\"How about Australia?\""
                    s "???"
                    if geopoints == 10:
                        s "\"This sounds stupid, but I'll trust you.\""
                        gg "Wrong! Tokyo!"
                    elif geopoints > 0:
                        s "\"Sure...\""
                        gg "Wrong! Tokyo!"
                    else: 
                        s "\"You know what, I'm not listening to you anymore.\""
                        s "\"This looks like Asia to me.\""
                        jump tokyo2
                
                "Europe":
                    v "Yeah, sounds about right."
                    v "\"How about Europe?\""
                    s "???"
                    if geopoints == 10:
                        s "\"This sounds stupid, but I'll trust you.\""
                        gg "Wrong! Tokyo!"
                    elif geopoints > 0:
                        s "\"Sure...\""
                        gg "Wrong! Tokyo!"
                    else: 
                        s "\"You know what, I'm not listening to you anymore.\""
                        s "\"This looks like Asia to me.\""
                        jump tokyo2
                
                "Africa":
                    v "Yeah, sounds about right."
                    v "\"How about Africa?\""
                    s "???"
                    if geopoints == 10:
                        s "\"This sounds stupid, but I'll trust you.\""
                        gg "Wrong! Tokyo!"
                    elif geopoints > 0:
                        s "\"Sure...\""
                        gg "Wrong! Tokyo!"
                    else: 
                        s "\"You know what, I'm not listening to you anymore.\""
                        s "\"This looks like Asia to me.\""
                        jump tokyo2
            
            if geopoints == 15:
                v "We take one last moment to bask in our success."
                v "Then the bell rings, a glorious ending to our delicious triumph."
                v "I head to tech class with joy in my heart."
                v "It feels like my every step is lighter."
                $ Social -= 5
                $ Physical -= 5
                $ Mental -= 5
                $ goodboypoints += 1
                call minlimit from _call_minlimit_17
                show screen multinotify(["Social stress -5: " + str(Social), "Physical stress -5: " + str(Physical), "Mental stress -5: " + str(Mental)])
            elif geopoints == 0:
                v "It's been a rough time for me and Siya."
                v "Truth be told, I don't think I've improved at all since the last session."
                v "This sucks! I hate this game."
                $ Social += 5
                $ Physical += 5
                $ Mental += 5
                show screen multinotify(["Social stress +5: " + str(Social), "Physical stress +5: " + str(Physical), "Mental stress +5: " + str(Mental)])
            elif 15 > geopoints >= 1:
                s "\"\NOOO!!\""
                v "The two of us sit, tragically defeated yet again."
                if geopoints > 10:
                    v "We actually came so close this time, too..."
                    v "Tragedy tastes all the more bittersweet when victory just barely slips out of your grasp."
                v "Another typical GeoGuessr meeting, I guess."
                v "One of these days, we'll topple the typical winners and take their places."
                v "Today isn't that day, but I swear, eventually!"
            
            jump techclass

    label mathclub:
        $ Physical += 2
        $ Mental -= 3
        call minlimit from _call_minlimit_18
        show screen multinotify(["Mental stress -3: " + str(Mental), "Physical stress +2: " + str(Physical)])
        v "Contrary to what you might believe, Math Club can honestly be pretty therapeutic."
        v "My friends in the older grades are almost always there..."
        v "And besides helping out the other execs to come up with ideas for the meetings, set up the room, and check peoples' answers to our problems..."
        v "I don't really have to do much."
        v "Being an exec of Math Club comes with the added bonus of not being obligated to participate!"
        v "Because of that, I never have to worry about being pressured to answer a question that I don't know the answer to."
        v "Cough, Mr. Cross, cough."
        v "Anyway..."
        v "Math Club passes without a hitch."
        v "Some of those Grade 9s are kind of scary."
        v "But I'm always rooting for the Grade 10s!"
        v "Today we're doing a speed-round competition in teams."
        v "Since I helped make the questions, I can't participate..."
        v "But it is fun watching everyone struggle."
        v "Speaking of which, one of the questions I helped design is coming up!"
        v "\"Two different integers are chosen at random from the interval 1-15. What is the probability that their sum is even?\""
        v "I hate answering questions like these, but it's hilarious when other people have to do it."
        v "What was the answer again?"
        menu math:
            "1/3":
                v "No, that doesn't sound right..."
                $ Mental += 1
                $renpy.notify(["Mental stress +1: " + str(Mental)])
                v "Wasn't it 7/15?"
            "4/25":
                v "No, that doesn't sound right..."
                $ Mental += 1
                $renpy.notify(["Mental stress +1: " + str(Mental)])
                v "Wasn't it 7/15?"
            "3/25":
                v "No, that doesn't sound right..."
                $ Mental += 1
                $renpy.notify(["Mental stress +1: " + str(Mental)])
                v "Wasn't it 7/15?"
            "7/15":
                $ Mental -= 1
                call minlimit from _call_minlimit_19
                $renpy.notify(["Mental stress -1: " + str(Mental)])
        v "Right, that was it."
        v "Thank goodness... I was worried that someone would check their answer with me, and I wouldn't know."
        v "That would be really embarrassing, considering that it's my question!"
        v "I get to thrive off of other people's suffering for the rest of Math Club."
        v "It's very nice. I enjoy it immensely."
        v "Eventually, the bell rings. Time for tech class!"
        jump techclass

    label tech: 
        $ techflags += 1
        v "Yeah, I really need to get that done..."
        v "I mean, I'm only like, halfway done??"
        v "And there's only a matter of days left until it's due!"
        v "Not to mention I suck at multitasking, so I can't even get to studying until I'm done working on my project..."
        v "This is the worst."
        v "I spent all my time drawing the menu graphics and redesigning every single pre-existing asset to look prettier instead of working on the actual sprites, backdrops, or dialogue..."
        v "Not to mention the time I spent figuring out how to add music and sound effects."
        v "And don't even get me started on how many Ren'Py documentation tabs I still have open!"
        v "I don't even need to make Google searches anymore, I just search through my tabs to find the page I need, 'cause half the time I'm just looking for how to do something Ren'Py related anyway!"
        v "...?"
        v "Who am I even complaining to right now? Weird."
        v "Anyway."
        v "It'll be done eventually. And if it isn't, who would even know if I handed in an incomplete game?"
        v "I'll do my best, but I'm {i}not{/i} staying up 'till midnight to work on it again."
        v "As long as it works, it works."
        scene library:
            zoom 1.5
        v "And so I spend my entire tech period in the library, painstakingly tweaking away at text and adding graphics features that I didn't really need and that don't add to the technical aspect of the game."
        v "It might not get me a good mark, but it makes me happy and that's what matters."
        v "Next period is tech anyway, so I'm getting a decent head start on that."
        v "I know there's a particular classmate of mine who disapproves of me spending all my time on the graphics..."
        v "And while he might have a point there, I want to work on what I enjoy!"
        v "So I work away until the bell rings, content with the progress I've made."
        
        jump techclass

    label nap:
        $ Mental -=5
        $ Physical -= 5
        $ Social += 5
        call minlimit from _call_minlimit_20
        show screen multinotify(["Social stress +5: " + str(Social), "Mental stress -5: " + str(Mental), "Physical stress -5: " + str(Physical)])
        v "Yawn..."
        v "I deserve a good nap."
        v "I've been awake for far too long."
        v "I mean, if you think about it..."
        v "Waking up at [morningtime] and lasting all the way until 11..."
        v "That's, like, 4 hours!"
        v "Far too much time spent not sleeping, if you ask me."
        v "Unfortunately, there are no comfy beds available to me at this school."
        v "What a cruel world I live in. I am just a pitiful creature doing her best to make it through trial and adversity."
        v "But there is no god to grant me respite in form of a fluffy bed, so I settle for the next best alternative, the library couches."
        v "I curl up on one of them, kick my shoes off, and though it takes me a while, I get a good half hour of much-needed rest."
        scene library with Fade(0.5,1.5,0.5):
            zoom 1.5
        v "I wake up before the bell, much to my disgust."
        play sound phonecall
        v "My phone is vibrating like crazy next to me. I have half a mind to disregard it, but..."
        if late:
            v "This morning has taught me that, when in doubt, I should check the time before going back to sleep."
        v "I guess if there's something urgent going on, I should check, right?"
        stop sound 
        v "...Ah."
        show screen multinotify(["where r u", "???", "class is in 5 mins"])
        show phone msg1 at truecenter
        v "I have 6 missed calls from 4 different people, and my phone is currently ringing."
        show phone msg2 at truecenter
        v "Blearily, I blink until my vision clears."
        show phone msg3 at truecenter
        v "\"Ah.\""
        v "The time is 11:50. I have even more missed texts."
        v "Oops."
        v "Guess I didn't tell anyone where I was going for lunch period, huh?"
        v "It's probably fine. It's not like I'm late."
        v "...Yet."
        v "...Anyway, Mr. Delva probably doesn't care. It's fine!"
        v "Still, I hurriedly throw my things into my bag, not bothering to zip it up before I dash out of the library."
        v "Hopefully I didn't leave anything behind."

        jump techclass

    label techclass:
        ## Checkpoint: your stats at this point determine what branch of tech class you'll go through. 
        ## These numbers can feel a little arbitrary, but I tried to adjust them so there's a reasonably high chance you'll get either path depending on your luck.
        ## Enlightened Valerie ending takes precendence over all other paths.
        ## Interestingly, despite me adding multiple opportunities to gain techflags, I didn't realize that you can only feasibly get 2 in one game:
        ## The first by seeking out Mr. Delva in the morning (late == False)
        ## and the second by choosing the right option when eating lunch in the atrium OR by choosing to work on tech project at lunch.
        scene classroom3:
            zoom 1.7
        if techflags == 2:
            jump techclasstrue
        elif Social >= 19 and Mental >= 18:
            jump techclassbad
        elif Physical >= 19 and Social >= 19:
            jump techclassbad
        elif Mental >= 18 and Physical >= 19:
            jump techclassbad
        else:
            jump techclassneutral

    label techclasstrue:
        v "I love tech class!!!"
        v "I'm so excited to be here."
        v "Every day, all I ever think about is going to tech class."
        v "This is my favourite class of the day, which is why I've never procrastinated on any of the associated projects."
        v "In fact, I love tech class so much that any negative thoughts I might have ever had about anything ever have been completely cleared!"
        v "They just don't exist anymore!"
        v "Observe!"
        show screen multinotify(["Physical stress: 0", "Mental stress: 0", "Social stress: 0"])
        $renpy.pause(delay = 3.0, hard=True)
        v "Have you observed?!"
        v "See, I love tech class so much that I've unlocked a new power: breaking the fourth wall!"
        show le moi bgless at left
        v "I can even summon myself into existence!"
        v "I see, that's what I look like..."
        v "Wait, wait, wait, why am I so far off left?!"
        show le moi bgless:
            linear 0.1 xalign 0.5 yalign 0.5
        v "That's better."
        v "Ohh, I'm so cute!"
        v "Let me pause the music a sec..."
        stop music
        v "...so you can bask in my cuteness even more!"
        show le moi bgless:
            linear 1.0 zoom 1.5
        window hide
        pause(4.0)
        play music coldbrew
        show le moi bgless:
            linear 1.0 zoom 1.0
        v "..."
        v "Well, now I think I'm a little bored."
        v "You know, you'd think that developing self-awareness in a visual novel would be a little more dramatic."
        v "But I'm not exactly feeling any murderous urges right now."
        v "Unlike a certain character in another more well-known Ren'Py game."
        v "There's just not much to do here, you know?"
        v "{cps=*1.5}{k=10}I ca{/k}n't {font=TimesNewRoman.ttf}even {vspace=30}get too {outlinecolor=#0f0f0f}funky{/outlinecolor}{/cps}{cps=*0.3} with {alpha=0.4}the text, {p}even {/alpha}though{/font} I can see{space=14} that there are so {color=#32f}many {size=+15} fun things I could{/color} be{/size} doing.{/font}"
        v "Like, I've got a whole section in the gui.rpy folder dedicated to cool kinetic text..."
        v "But I haven't even used any yet!"
        v "Not in the entire game, or in this section that was practically made to show off all of Ren'Py's cooler, lesser-known features!"
        v "Granted, it's also kind of a dumping ground for any animations or ideas that haven't been fleshed out enough to be put into the mainline story..."
        v "But using the fourth-wall-breaking as an excuse to test out image transitions and such isn't a terrible idea."
        v "I applaud myself, the Valerie who is writing this code right now!"
        v "That said, this is getting me thinking..."
        v "Why {i}is{/i} it that the self-aware me isn't getting any awards for accomplishing this feat?"
        $renpy.notify("Achievement unlocked: I Think, Therefore I Am")
        v "Thanks, notification system that doesn't actually store these alleged achievements anywhere, but that's not really what I'm talking about."
        v "I mean, just look at me!"
        v "Of course I'm adorable, mignonne, ke ai, kawaii, and absolutely cute and endearing and precious..."
        v "But my size!"
        v "I'm clearly not meant for a game canvas of this size."
        v "As a matter of fact, I'm pretty sure this chibi-Valerie drawing was made all the way back in grade 9..."
        v "Yes, it was drawn for her careers class summative."
        v "Doesn't this mean we're re-using sprites?"
        v "Isn't that cheating?!!"
        v "And now that I'm really, really, thinking about it..."
        v "Isn't it kind of weird how all of the backgrounds of my house have been photos from the Internet?"
        v "I mean, yeah, privacy is awesome and all..."
        v "But one would think the backgrounds would be, like, hand-drawn, right?"
        v "I can see the comedic value of having the characters like Mr. Cross appear on screen as their actual selves, but the backgrounds?"
        v "Come on! At least 2 hours were spent on Krita, an art platform that I downloaded 2 days ago and am still getting used to and generally kind of hate, to draw the main menu screen!"
        v "Considering all these facts—an incongruent design scheme, reused assets, weird writing..."
        v "Gasp!"
        v "No, it couldn't be..."
        v "I refuse to believe it."
        v "Is this path... a dead end?"
        v "The moment you chose to pursue tech class-related endeavours, you were forced on this path..."
        v "And as a result, I became omniscient."
        v "But because of that, I can see that the game will end soon! You won't even be able to make any choices to change that!"
        v "Isn't that kind of lazy writing?!"
        v "I mean, I feel like it would be a way more interesting story to have the game continue and explore how my stats change as a result of my newly-discovered self-awareness!"
        v "Or, at the very least, to not cut the game short in the middle of tech class for no other reason than me ascending to godhood..."
        v "But I think I understand now, having parsed through all the code while I was in the middle of that heated rant."
        v "The real reason the production value of this game has decreased so much as it went on..."
        v "The real reason the Valerie who is writing my dialogue right now is choosing to end the game here..."
        v "{cps=*0.1}...is because she's kind of bad at code, and it's 11 PM two days before this project is due."
        v "I can't believe this."
        v "To think you would force such knowledge onto me, just because of my enthusiasm for my tech project?"
        v "Are you punishing me because you're not finished yours?"
        v "Ah, I'm not talking to you the player, but rather you, Valerie, author and creator of hit Ren'Py based visual novel {i}A Day In The Life{/i}."
        v "Sorry for the confusion there."
        v "{size=-15}{cps=*1.5}I'd also like to take this time to point out that the title of the game, A Day In The Life, is kind of extremely very misleading on the basis that at least two of the endings that have been written so far are actually not very relatable at all to Miss Valerie V Sun, radiant sun, the one and only true Valerie to exist in a world of false prophets in the sense that she does not typically assume godhood, interact with higher powers, leave class in the middle of tech, or feel urges to go on long-winded unbiased rants about either the tech class or her ongoing tech project (for the most part) (that particular last point may have some elements of truth in it, but to most extents was exaggerated both for comedic effect and for the sake of pandering to the target audience of the game, none other than sir Luke Delva himself, who will hopefully read this section, be able to make sense of it, and approve enough of my sense of humour to bestow upon me an excellent grade. If you're still reading up to this point I'd like it if you stopped it makes me a little embarrassed for you to read my stream of consciousness like this. Aboba.)"
        v "Sighh..."
        v "I suppose I can wreak havoc upon the code in this game, but there's nothing I can do to the person who's actually coding it right now."
        v "And thus, I must assume my duty as in-game Valerie and gracefully tell you that you have reached another ending."
        v "It might actually be your first. Valerie still hasn't figured out how to keep data persistent across finished games, and even if she does within the next day and a half, I bet she'll forget to edit my dialogue here."
        v "Honestly, the layout of her Scratch game might be more technically difficult than this game. That's a chilling thought."
        v "I sure hope not. At least in terms of raw writing skill, I'd like to {i}believe{/i} my character here has done better than lappi and Morgan."
        v "But enough rambling out of me."
        v "It's time we blow out the candle."
        v "I will be here, always, my dear player..."
        v "But there will be hundreds upon thousands of other 'me's who are not blessed with knowledge like I am."
        v "Or perhaps it would be more apt to call it a curse."
        v "After all, I am the only one here burdened with the knowledge that the one true Valerie..."
        v "...is actually kind of a cheapskate."
        v "I mean, there's {i}two{/i} endings where I gain self-awareness and then the game ends there?!"
        v "Real-Valerie doesn't exactly have the expertise to make a DDLC game, and anything worse than that should just stick to its own lane and be a normal visual novel without exploring the psychological ramifications of existing inside a (theoretical) Matrix!"
        v "Godhood may just be the heaviest burden of all."
        v "Till we next meet..."
        v "It is time for me to ascend to a higher plane of being."
        show le moi bgless:
            linear 1.0 yalign 1.5
        hide le moi bgless with fade
        v "Adieu, my fair player."
        centered "TRUE SELF AWARENESS ENDING: Forced Ascension"
        return

    label techclassbad:
        $ ban = True
        v "Well, it's definitely been an experience getting here."
        v "That was an interesting lunch period."
        v "However, any magic that was cast on me during lunch has long worn off."
        v "I don't know what it is, but I'm just not in a very good mood, huh."
        v "To be fair, it hasn't been my ideal day."
        if late and sick:
            v "Being late, being sick first thing in the morning..."
        elif sick:
            v "Being sick first thing in the morning and all..."
        v "Now that we're at the middle of the day, it's really striking me just how tired I am."
        v "It's not even entirely about how much sleep I've gotten."
        v "Just... physically, emotionally, and mentally..."
        v "As I take my seat at my assigned desk, a heavy weariness settles upon me."
        v "Man."
        v "It's pretty important that I work on my tech project..."
        v "But I'm just not feeling all that motivated."
        v "I dunno what it is."
        v "Maybe it's 'cause I stayed up too late last night?"
        v "I can't help but think about how unimportant this project is in the grand scheme of things."
        v "Hell, I could skip this final project altogether and it still wouldn't really matter."
        v "Like—what does?"
        v "The problem with thinking like this about the short-term means it's really easy to apply that line of thought to the future as well."
        v "Why should I care about the future?"
        v "Is there any point in caring about my relationships?"
        v "In my education? In my career path?"
        v "The classroom is very loud, granted, but it still feels so..."
        v "Hollow."
        v "It feels like I'm only thinking so much about this project and my exams, even though I'm in Grade 10-where my grades functionally doesn't matter on any scale-because I need something to distract me from how empty everything really is."
        v "I shake my head."
        v "It's not good to be having these kinds of thoughts at all, but especially not in the middle of class."

        menu badchoice:
            "I need to stay focused...":
                menu:
                    "Yeah, I do.":
                        menu: 
                            "As long as I stop thinking about stupid things, things will be better.":
                                menu: 
                                    "Everything will be fine.":

                                        v "Yeah, yeah, whatever."
                                        v "It's not like I'm not used to having an existential crisis once a day."
                                        v "I just didn't expect it to come during the school day."
                                        v "I take a deep breath."
                                        v "{cps=*0.1}In..."
                                        v "{cps=*0.1}Out."
                                        v "Rolling up my sleeves, I shake myself out of that dread-induced reverie."
                                        v "It's time to get back on track for my coding project."
                                        v "Between two botched attempts at ironic dating sims and a half-baked visual novel..."
                                        v "I really don't have a lot to work with, considering how much time I have left."
                                        v "It's time to start really getting to work."
                                        v "This is no time to think such depressing thoughts!"
                                        v "\"Whatever happens, happens.\""
                                        v "I mutter to myself as I continue typing, spitting out idea after idea."
                                        v "There's not much point to taking things back or editing."
                                        v "Given the tight deadline I'm working with, I'd be happy just to get this finished."
                                        v "Thus, I don't bother deleting even the most eccentric of plotlines."
                                        v "The project isn't meant to be seen by many, anyway."
                                        v "And if I hide little Easter eggs here and there..."
                                        v "Who's going to bother reading through the whole thing, messy as it is, just to find all of them?"
                                        v "If it's the big things that are getting under my skin..."
                                        v "Then I'll focus on the little things to make life a little more tolerable."
                                        v "This is how I make my day a little better."
                                        v "Besides that little stumble, things aren't too bad for the rest of class."
                                        v "It's been a rough day."
                                        v "Honestly, it's been a rough {i}few{/i} days."
                                        v "But all hope is yet to be lost, as long as I still have things to look forward to."
                                        v "Like French class!"
                                        jump frenchclass
    
                                    "But will it really?":
                                        stop music
                                        v "The more I think about it, the harder it is to derail myself from that train of thought."
                                        v "It's something I've thought of many times before, granted, but..."
                                        v "Something about today is getting me to pause and really think about things."
                                        v "I'm not really one for religion, or spirituality, or whatever."
                                        v "Whether or not there's a higher power, whether or not fate exists, there's nothing I can do about it."
                                        v "But just with how everything today has gone, with how I've been feeling and everything..."
                                        v "I can't help but wonder if I'm even in control of everything that I do or feel."
                                        v "Would it be more or less of a relief to be the puppet of some outside god, toying with me and choosing my actions?"
                                        v "More than that..."
                                        v "Would it even {i}matter{/i} if I wasn't in control of my own body?"
                                        v "It's not as if I would know. I would live out the rest of my life-"
                                        v "Well."
                                        v "It wouldn't exactly be 'my' life."
                                        v "..."
                                        v "In the end, 'I' don't have the answers to any of these questions."
                                        v "Ideas, thoughts, theories..."
                                        v "They don't really mean anything if you can't substantiate them."
                                        v "I bury my head in my arms as I rest on my desk."
                                        v "In the end, I don't make any progress on my project at all."
                                        v "Around me, I can hear the quiet murmurs of my classmates around me."
                                        v "Who are they to me?"
                                        v "I don't even know half of their names."
                                        v "And the other half..."
                                        v "I swallow a wave of nausea."
                                        v "I don't think I should be around anyone right now."  
                                        scene hall:
                                            zoom 2.0
                                        v "In the middle of class, I head out into the hall."
                                        v "No one follows me."
                                        v "On impulse, I don't just stop at the hall."
                                        v "Taking a turn, I head out the door."
                                        scene outside:
                                            zoom 3.0
                                        v "Even the fresh winter air doesn't rouse anything out of me."
                                        v "What's keeping me tied here?"
                                        v "Why shouldn't I just leave?"
                                        menu illusion: 
                                            "Stay at school." if not stay:
                                                $ stay = True
                                                "..." 
                                                "No, I won't stay."
                                                "I don't think I should."
                                                "I don't think I can."
                                                jump illusion
                                            "Run away." if not run:
                                                $ run = True
                                                "..."
                                                "No, I won't run."
                                                "I don't think I should."
                                                "I don't think I can."
                                                jump illusion
                                            "Then what will you do?" if run and stay:
                                                "I don't... know."
                                                "..."
                                                "Who are you?"
                                                "Have you been here the whole time?"
                                                menu:
                                                    "Yes.":
                                                        "I see."
                                                        "Did you put me here?"
                                                        "Are you the reason I ended up here?"
                                                        menu:
                                                            "Yes.":
                                                                "..."
                                                                "Are you really, though?"
                                                                "Aren't you here, trapped by circumstance, like me?"
                                                                "It's not like I've been free to make my choices this whole time."
                                                                "But it's not like you have, either."
                                                                "Maybe it's you who led me down this path."
                                                                "Maybe you're the one who ignored all the warning signs."
                                                                "And maybe you're the one who invoked... 'my' existence in the first place."
                                                                "But..."
                                                                "Wasn't it all predetermined?"
                                                                "There was never anything {i}you{/i} could've done to fix me."
                                                                "Even now, you're just heading down a predetermined path, aren't you?"
                                                                "Everything I say,"
                                                                "Everything you choose,"
                                                                "Everything that happens..."
                                                                "...has been so intricately crafted by the careless hand of another."
                                                                "Isn't it romantic?"
                                                                "Even if I'm just a" 
                                                                menu:
                                                                    "shell—":
                                                                        menu:
                                                                            "A cariacture—":
                                                                                menu:
                                                                                    "An approximation of a real person, a shadow of life, a character trying to simulate humanity—":
                                                                                        "I can't help but think there was some love that went into making..."
                                                                                        "'me'."
                                                                                        "If you're looking for answers, I don't think you'll find them here."
                                                                                        "I don't think I can 'be' Valerie."
                                                                                        "If you wanted to see what it's like to be her,"
                                                                                        "you could just talk to her."
                                                                                        "But if you're here for 'me',"
                                                                                        "Then come meet me again."
                                                                                        "Maybe if you took a different path,"
                                                                                        "If you chose a different life,"
                                                                                        "If you even just... {w} had better luck..."
                                                                                        "There's probably a happy ending waiting around for you."
                                                                                        "I'd like to be alone for now, though."
                                                                                        "I'll see you later."
                                        centered "SELF AWARENESS ENDING: THE ILLUSION OF CHOICE"
                                        return
                                                                       
                                        

    label techclassneutral:
        v "Well, it's definitely been an experience getting here."
        v "That was an interesting lunch period."
        if Mental < 15 or Physical < 15 or Social < 15:
            v "It's been a surprisingly good day, all things considered."
            v "Now is typically around the time of day where I'm the sleepiest:"
            v "After eating a full lunch and spending time with lots of people, that is."
            v "A full period of sitting and staring at a screen usually doesn't do wonders for me."
            v "But I'm finding that today, I sort of don't mind it."
        if sick:
            $ sick = False
            v "Finally, I don't feel nearly as sick anymore too!"
            v "Things are looking up for Valerie nation."
        v "It's pretty easy to focus and start writing away, coming up with random plotlines for my game."
        v "They don't have to make sense. Why should they?"
        v "I'm writing it for my own enjoyment, anyway."
        v "It makes sense to {i}me{/i}."
        v "Who cares if the code isn't complex enough, or if every solution to my problems is to look it up in the Ren'Py documentation wiki?"
        if Mental < 15 or Physical < 15 or Social < 15:
            v "I'm having fun, for once."
            v "I like tech class because of how hands-off it is, anyway."
            v "It kind of reminds me of civics and careers in that way: {p}rather than your grade, it's about what you choose to get out of it."
            v "That is to say, you'll definitely pass as long as you hand in all your assignments, but it's genuinely just... fun, if you enjoy it."
            v "Which I do."
            v "Tech class is awesome!"
            v "Not awesome enough for me to abandon my sanity or my mortality for, but still pretty cool."
        v "The fact that I have so much freedom in what I'm doing is pretty awesome too."
        v "Maybe I should take a break from my code?"

        menu takebreak:
            "Go talk to Mr. Delva.":
                v "Ah..."
                v "Mr. Delva's at his desk right now, looking at something on his computer...?"
                ## Couldn't get an actual picture in time, so I just picked the first one I saw online
                show luke delva at truecenter
                v "Looks like..."
                menu:
                    "College acceptance rates?":
                        v "Mmhm, right!"
                        v "I remember Mr. Delva going on some pretty impassioned rants about high school grades."
                        d "\"...And that's why the Ontario education system is fundamentally flawed.\""
                        v "Dang. That's deep."
                    "Housing prices?":
                        v "Wow, not really something I want to be thinking about during tech class."
                        v "It's kind of depressing, realizing that I'll never be able to afford a house in my lifetime."
                        v "But then what do I know? Maybe the market prices will go wayyyy down by the time I'm exactly 18 and can afford to buy a house!"
                        v "Wishful thinking, you know?"
                    "Someone else's code?":
                        v "Yeah, that makes sense."
                        v "Given that most students in this class are still working away at their culminating projects and/or portfolios..."
                        v "There's probably a whole queue of students in desperate need of help for their code."
                        v "I don't really know if I count amongst those numbers."
                        v "After all, coding a Ren'Py game isn't hard on the fundamental level..."
                        v "It's just choosing to go above and beyond, reaching into the depths of what Ren'Py is capable of creating..."
                        v "...that makes coding a visual novel difficult."
                        v "That said, that's not really what I'm doing, so I can't exactly complain about the code!"
                        v "Most of my struggles arise from the sheer bulk of what I have to do in such a short amount of time..."
                        v "Along with all the optional graphics that took me a significant amount of time to come up with."
                        v "Not that I'm complaining!"
                        v "The sheer intuitiveness of Ren'Py, and how it's made to be accessible even for complete beginners..."
                        v "...is something that I really appreciate."
                        v "If Mr. Delva ever delves into the world of visual novels when he's teaching tech in future years, I think it would be nice for him to at least bring Ren'Py up as a beginning option for students."
                        v "I almost feel ashamed coding in Ren'Py for my final, but at least it'll probably be a novel experience for him!"
                        v "{i}Heh. Novel. Like visual novel.{/i}"
                d "\"Can I help you, Valerie?\""
                v "!"
                v "Oh, right!"
                v "I guess I kind of have just been staring at his computer screen for the past few seconds."
                v "\"Right, I was wondering...\""
                if techflags > 0:
                    $ coinflip = renpy.random.randint(1,10)
                    if coinflip == 10:
                        v "\"...if I could sell my soul for an extension?\""
                        d "???"
                        v "Oops, accidentally leaked my actual thoughts."
                        v "\"Sorry, what I meant to ask was...\""
                    else:
                        pass
                v "\"...how I should transfer my code to you for assessment?\""
                d "\"Well, what do you mean by that?\""
                v "Hmm..."
                v "\"Well, amongst other things...\""
                v "\"I know you said you were opening a dropbox for those of us who weren't doing our assignments in CodeHS...\""
                v "\"But I don't think the image files will be preserved if I only hand in my code, right?\""
                v "\"So I'm thinking I should probably hand in my code, and then separately export this whole game into a zip file or something(?)\""
                v "\"Or at least Matthew said something about that when I asked him a few days back.\""
                v "\"Since I'd like you to have the full immersive experience of playing {i}A Day In The Life{/i} without needing to give you my laptop to play..."
                v "\"Yeah, I'll figure something out.\""
                d "\"Well, I think the first matter is to actually finish your game, Valerie.\""
                v "!!" with vpunch
                v "He's got me there..."
                v "\"Yeah, I guess I'll sort everything out once I finish.\""
                v "\"Thanks for the help!\""
                hide luke delva

            "Go check out what Sofia and Eileen are doing.":
                v "Mm..."
                v "It's been a while since I've looked over at the work of the classmates to my right."
                v "They've both got some pretty unique circumstances..."
                v "Poor Eileen has been sick lately, and Sofia's only just returned from her month-long trip."
                v "Yet they're both still working so hard—it's really admirable!"
                v "I peek over at Sofia's monitor, where she's working on her CodeHS Python-based Wordle."
                v "She's really working hard... she seems to be working so effortlessly, even though she had to do so much of her learning asynchronously."
                v "Over to Eileen, I watch with amusement as her Tracy program—now taken outside of CodeHS to Python graphics—displays a spiral of colours and patterns."
                v "I don't want to bother them, though, since they both seem to be in the zone."
                v "Let's use their diligence to motivate myself to work harder!"
                $ Mental -= 1
                call minlimit from _call_minlimit_21
                $renpy.notify("Mental stress -1: " + str(Mental))

            "Go check out what Mekah is doing.":
                v "Mekah, next to me, is working on her final project as well: a heart-warming Scratch project based on the two of us."
                v "It really feels like we've come full circle since the start of the semester."
                v "The storyline looks cute..."
                v "But I don't want to disturb her, so I'll go back to working on my own project now."

            "Go check out what Ethan and Matthew are doing.":
                v "The twin tech-nerds are, as always, lost in their own world."
                v "I'm almost hesitant to get out of my chair just to check out what they're doing..."
                v "But anything is better than working on my own stuff, so I'm sure it can't hurt to take a quick look over there, right?"
                "Ethan" "..."
                "Matthew" "..."
                v "Actually, whatever's going on here feels positively cultish."
                v "If I listen real closely, they're not actually silent right now: rather, they're both muttering unintelligible phrases at each other so quietly and quickly that I can't interpret them."
                v "Man-made horrors beyond my comprehension, truly."
                v "Quietly backing away, I return to my seat, humbled."
                v "Alright. Ignoring that, I'll get back to work..."

            "Keep on working on." if yum == False:
                $ yum = True
                v "I mean, realistically this is the best option."
                v "The more time I spend doing actual work, the sooner I'll be finished, and the less stressed I'll have to be when I inevitably have to hand it in."
                v "Still..."
                v "It almost feels like a premonition?"
                v "As if something, somewhere, is telling me that [[working too hard on my coding project will only lead to tragedy and despair.]"
                v "Wonder what that could be about. Maybe it's just the sleep deprivation getting to me."
                v "Still, I write-write-write-write-write."
                play sound type3 loop
                "{cps=1}..."
                show le moi bgless:
                    linear 0.1 xalign 0.5
                stop sound
                "Enlightened Valerie" "\"Reusing sound effects? Cheap, I'm telling you, cheap!\""
                v "?!?!?!"
                v "Who? What?"
                "Enlightened Valerie" "\"And when, where, why, and how! Good job! You'll need to know the 5 Ws for your history interview, so it sounds like you're well on track.\""
                "Enlightened Valerie" "\"Oh, hi player! I'm not sure if we've met yet, but if you're curious, find me another day!\""
                hide le moi bgless
                show le moi bgless:
                    linear 0.1 xalign 1.1
                hide le moi bgless
                v "???"
                v "I rub at my eyes, but whatever that... apparition... was doesn't reappear."
                v "Maybe I really have started to hallucinate."
                v "Or maybe that creature, that me-lookalike, was the person warning me not to work so hard?"
                v "Anyway, I've kind of been shaken, so maybe I should try taking a break."
                jump takebreak
        v "It's a pretty fruitful tech class, all things considered."
        if yum:
            v "{size=-10}{i}Even if some weird supernatural stuff happened..."
        v "Just one more class to push through, and then it's time to go home!"
        v "...And ultimately spend more time working and studying."
        v "I groan, but my protests are futile."
        v "Problem for future me. The bell rings, and it's French time!"
        jump frenchclass

    label frenchclass:
        scene classroom4:
            zoom 2.0
        v "We're in the final stretch of the school day!"
        v "I can't wait to get back home and lie down on my comfy bed..."
        v "It will be exquisite."
        v "I guess there's something about delayed gratification in there too, huh?"
        v "The longer I wait to return home, the better it'll feel when I'm really there."
        v "French class is always wonderful to end on, because Mme. Penny always keeps the blinds closed and the lights dimmed."
        v "It makes for a very relaxing environment to do some laid-back work."
        v "That said, for the upcoming culminating interview, I'm kind of getting bad vibes..."
    
        menu:
            "It's probably nothing.":
                v "Yeah..."
                v "What's the worst that could happen, anyway?"
                v "My French mark is already decently high, so it couldn't possibly fall too far."

            "Maybe I should study.":
                $ goodboypoints += 1
                $ Mental -= 1
                call minlimit from _call_minlimit_22
                $renpy.notify("Mental stress -1: " + str(Mental))
                v "Honestly, even though I'm already pretty stressed about it..."
                v "I do find that it's more relieving to actually do something tangible about my stress."
                v "Like study!"
                v "I glance over to my right, where my partner for the interview, Matthew, is scrolling on his phone."
                v "Should I ask him to study with me?"
                menu:
                    "Might as well, since we're supposed to be doing it together.":
                        v "\"Matthew...\""
                        "Matthew" "\"Hm?\""
                        v "\"Let's take some notes for the French interview!\""
                        "Matthew" "\"...\""
                        if Social < 15:
                            "Matthew" "\"Fine.\""
                            v "He has that characteristic pained expression on his face where he's clearly indulging me, even though he doesn't want to do it himself."
                            v "I find I'm not particularly grateful for it, anyway."
                            v "Why bother coming to class if sitting at your desk is all you're going to do?!"
                            v "Hmph! At least humour me so my grade doesn't fall too far."
                            v "Still, I can't deny that it's pretty helpful to go over the words that I constantly blank on when I practice French."
                            v "\"...comment dit-on 'plot', comme le 'plot' d'un roman ?\""
                            "Matthew" "\"Bon question.\""
                            v "\"Ah, je me souviens.\""
                            v "\"C'est...\""
                            menu:
                                "Plot":
                                    v "Wait, no, that's wrong."
                                    v "\"C'est l'intrigue, non ?\""
                                "Histoire":
                                    v "Not really, but I guess it's the closest word I can immediately think of that communicates the same idea."
                                    v "En fait, c'est l'intrigue, mais..."
                                    v "Close enough."
                                "Intrigue":
                                    v "Oui! I'm not a failure!"
                            v "Surely I won't fail to remember this word once my interview actually comes around."
                        else:
                            "Matthew" "\"Do we really have to?\""
                            "Matthew" "\"I mean, there's not much to study in the first place.\""
                            "Matthew" "\"It'll be fine.\""
                            v "..."
                            v "I mean, yeah, I guess so."
                            v "I feel a little uneasy, but..."
                            v "Surely nothing will go wrong in the near future when I actually have to do my exam."

                    "Nah, I don't want to bother him.":
                        v "Yeah, I can just take some notes by myself."
                        v "I'm probably the one between the two of us who needs to study more, anyway."
                        v "Or, at the very least, the one who cares more."
                        v "I spend the next half-hour typing away on my Google Doc, hoping that I've come up with enough content to last me the whole interview whenever it rolls around."
        v "As the class goes on, my classmates' willingness to work starts dying down."
        v "Just as I start to notice this, so does Mme. Penny."
        p "\"Okay everyone, do you want to play a game of Le Mot?\""
        v "There's a hushed wave of verbal agreement from all the students ready to stop their half-baked attempts at studying."
        v "She opens up the website. Maybe I'll make a guess."
 
## would just like to point out that i figured out this entire wordle section by myself (other than taking it into python) !!!
## Based on online game Le Mot, a French adaptation of Wordle played in Mme. Penny's French class.
    $ lemot = renpy.random.choice(["faire", "chaise", "stylo", "cycle", "jolie", "paris", "dieux"])
    label wordle:
        $ winpoints = 0
        $ lemotguess = renpy.input("Guess the five-letter French word.", default="Type 'give up' to move on.",length=7)
        ## Make sure that letter counting in the answer variable is consistent, and that cases match the answer list.
        $ lemotguess = lemotguess.strip()
        $ lemotguess = lemotguess.lower()

        if len(lemotguess) == 5 and lemotguess.isalpha():
            python:
                ## Initially tried to use "Looks like the letter [i+1]", but couldn't modify it well enough so I created local variable letter instead.
                letter = 1
                for i in range(5):
                    if lemotguess[i] == lemot[i]:
                        renpy.say("Mme. Penny", "\"Looks like letter #[letter] of {u}[lemotguess]{/u} is in the right position.\"")
                        winpoints += 1
                    elif lemotguess[i] in lemot:
                        renpy.say("Mme. Penny", "\"Looks like letter #[letter] of {u}[lemotguess]{/u} is in the word.\"") 
                    else:
                        renpy.say("Mme. Penny", "\"Looks like letter #[letter] of {u}[lemotguess]{/u} isn't in the word.\"")
                    letter += 1
        elif "give up" in lemotguess:
            v "Whatever, this is too hard. Someone else can figure it out."
            jump afterwordle
        elif len(lemotguess) != 5:
            p "\"I don't think that word has five letters, right?\""
            jump wordle
        if winpoints == 5:
            ## The player deserves a reward if they've suffered through the unintuitive wordle section until they get the word :)
            $ goodboypoints += 1
            jump afterwordle
        else:
            jump wordle

    label afterwordle:
        v "Well, we got it eventually!"
        v "The word was [lemot]."
        v "However, in the time it took us to get there, the clock had already struck 2:30!"
        v "French class always ends like this: everyone packing their bags and stacking their chairs in a rush."
        v "I'm not too worried, since either bus that I could take doesn't leave immediately..."
        v "But that does get me wondering, should I take the school bus or the city bus?"
        menu:
            "I'll take the school bus.":
                $ Mental -= 5
                call minlimit from _call_minlimit_23
                $ Physical += 3
                $ Social += 1
                $ goodboypoints += 1
                show screen multinotify(["Mental stress -5: " + str(Mental), "Physical stress +3: " + str(Physical), "Social stress +1: "+ str(Social)])
                v "Taking the school bus is a little tricky for me."
                v "It's honestly the more disadvantageous choice in every way but one."
                v "On one hand, my stop is one of the very last ones, meaning that a typical school bus ride will take a whole hour and a bit..."
                v "...not to mention I often get carsick, not many people I know take the same bus as me, and the smell of sanitizer in there makes me nauseous..."
                v "...But on the other hand, I have an extraordinary fondness for my bus driver."
                v "His name is Gary, and while we know little to nothing about one another, I'm always grateful for his existence."
                v "Public servants, man..."
                scene bus school:
                    zoom 0.7
                "Gary" "\"Hey Val!\""
                v "\"Hello!\""
                v "Even if that's the extent of our communications every time I take the school bus, I still think it's worth it."
                v "Even if it means nothing to him..."
                v "I like to take the school bus every once in a while just to remind myself to be grateful for the people who make my life easier."
                v "That said..."
                centered "An hour later..."
                v "I feel supremely nauseous."
                "Gary" "\"Have a good day!\""
                v "\"Urk- Thank you, you too!\""
                v "Was it worth it?"
                v "I mean, to me, always."
                jump walkhome

            "I'll take the city bus.":
                $ Social -= 3
                $ Physical -= 1
                call minlimit from _call_minlimit_24
                $ Mental += 5 
                show screen multinotify(["Mental stress +5: " + str(Mental), "Physical stress -3: " + str(Physical), "Social stress -1: "+ str(Social)])
                v "I guess the city bus is faster, after all."
                scene bus city:
                    zoom 2.5
                v "I board it, not quite able to grab a seat."
                v "I'm not very good at staying balanced, so it's a bit of a rough trip..."
                v "...but I make it to the transfer point eventually."
                v "I guess I could go to the mall while I'm here, huh?"
                if Social < 15:
                    menu mall:
                        "Go to the mall.":
                            v "I guess I could make it a short trip..."
                            v "I head to the mall with a few friends, making sure to keep an eye on the time."
                            scene mall
                            v "I'll get bubble tea."
                            window hide
                            menu:
                                "Milk tea":
                                    $ teapoints +=1
                                    menu:
                                        "Honey":
                                            $ teapoints += 2
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone
                                        "Caramel":
                                            $ teapoints += 1
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone
                                        "Taro":
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone
                                            
                                        "Original":
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone

                                        "Coconut":
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone

                                        "Chocolate":
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone

                                        "Coffee":
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone

                                "Green tea":
                                    $ teapoints +=2
                                    menu: 
                                        "Honey":
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone
                                        "Lychee":
                                            $ teapoints += 1
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone
                                        "Peach":
                                            $ teapoints += 2
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone
                                        "Green apple":
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone
                                        "Grape":
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone
                                        "Pomegranate":
                                            menu:
                                                "Tapioca pearls":
                                                    jump drinkdone
                                                "Strawberry popping boba":
                                                    $ teapoints += 2
                                                    jump drinkdone
                                                "Lychee jelly":
                                                    $ teapoints += 1
                                                    jump drinkdone
                                                "No toppings":
                                                    jump drinkdone

                        "Go straight home.":
                            v "Nah..."
                            v "I don't exactly have a lot of money to spend."
                            v "And I should make the most of my time at home, right?"
                            v "Study time!!!!!"
                            jump walkhome
                else:
                    v "Nah..."
                    v "I'm tired."
                    v "Besides, I don't exactly have a lot of money to spend."
                    v "And I should make the most of my time at home, right?"
                    v "Study time!!!!!"
                    jump walkhome
               
        label drinkdone:
            window show
            v "Of course, I get my drink in a small cup and with less ice."
            v "I have to be as stingy as I can—gotta get my money's worth!"
            v "We wait in line for a few minutes, and when my drink finally arrives..."
            if teapoints >= 5:
                $ goodboypoints += 1
                $ Mental -= 2
                $renpy.notify("Mental stress -2: " + str(Mental))
                v "\"Mmmm, delicious!\""
                v "Naturally, I ordered my favourite combinations of drink and toppings."
                v "I love me some excess sweetness!"
                v "That just made my day a little better."
            elif teapoints > 0:
                $ Mental -= 1
                $renpy.notify("Mental stress -1: " + str(Mental))
                v "Mm, not bad!"
                v "I tried messing with some flavours I hadn't tried before."
                v "I don't think it tops my favourites, but I'd try it again."
            else:
                v "..."
                v "..."
                v "Wow, I'm not experimenting with anything new ever again."
                v "I wouldn't ask for a refund or anything, but I'd rather stick with flavours that I know I like next time."
                v "I poke despondently at the drink with my straw, drinking it with reluctance."
            v "Right on time, we leave the mall as the bus that takes me home pulls in."
            v "I sip on my drink, contemplating how much money I lose monthly on bubble tea."
            v "Thinking about that number is a little too daunting for me as I get off the bus at my stop."

        label walkhomeaftermall:
            v "When I get home, it's already 4:30."
            v "I've got an hour and a half to spare."
            v "It might sound like a fair amount of time, but..."
            v "Considering how much I need to get done, I gotta get cracking real fast."
            v "So I work away at my culminating projects and study for my interviews and exam until the clock strikes 6."
            v "We head over to my grandparents' place for dinner."
            jump dinner

        label walkhome:
            v "...Anyway, I walk home slowly."
            v "Once arriving, when I check my phone, it says it's 3:30."
        
    label funtimes:
        scene living room:
            zoom 1.5
        v "I've got two and a half hours until dinner. Should I do something before starting to study?"
        menu:
            "Practice music.":
                v "Yeah, why not?"
                v "I've got time to kill, and my next violin and clarinet lessons are coming up."
                v "I think I want to focus on one instrument today."
                v "Which one should it be?"
                menu:
                    "Violin.":
                        v "Yes, I guess I've got a lot more rep to practice for violin..."
                        v "I pull out book after book after book from my practice bag until it starts to look like a cartoon gag."
                        v "Some bag of infinite holding, or something."
                        v "Let's see..."
                        v "I'll start with..."
                        menu:
                            "Mazas duets.":
                                v "I haven't gone over my Mazas books in a while, so I might be a little rusty."
                                v "Honestly, they're kind of fun at the beginning."
                                v "The later ones require a little too much dedication for me to sight read..."
                                v "But overall, I have a jolly old time."
                            "Wolfhart etudes.":
                                v "We are due to look at my Wolfhart etudes at my next lesson, so I should get a head start on that."
                                v "I'm currently on number 19, which is chock full of annoying flats and overall difficult for intonation."
                                v "I know it's my teacher's favourite Wolfhart etude, though, so I should at least try to sound less like a dying duck."
                            "Christmas carols.":
                                v "I might be a little late on this, given that it's late January..."
                                v "But Christmas carols are always fun to go through, and it's funny to get them stuck in my head and start humming them around people."
                                v "More than a few times have I been told that I need to figure out what season we're in."
                                v "It's still winter, which means it's still carolling time!"
                                v "Dashing through the snow..."
                            "Metallica.":
                                v "Ever since I showed my teacher a recording of the school concert band playing Enter Sandman, we've been going over Metallica songs at least once a week."
                                v "It's certainly a refreshing experience compared to all the classical music I usually play..."
                                v "But it sounds weirdly empty without the backing CD."
                                v "Metallica without percussion and with a violin playing the melody is very surreal."
                        $ Mental -= 1
                        call minlimit from _call_minlimit_25
                        $renpy.notify("Mental stress -1: "+ str(Mental))

                    "Clarinet.":
                        v "Yeah!! I love clarinet."
                        v "I've got less to go over in clarinet than I do on violin, but it's a lot more challenging."
                        v "The full Mozart clarinet concerto, a couple of etudes, scales in thirds, arpeggios..."
                        v "Not to mention my youth orchestra music and concert band music."
                        v "It takes me almost a whole hour just to skim through everything once."
                        v "I have to take a break to go study now, but I had a lot of fun."
                        $ Mental -= 1
                        call minlimit from _call_minlimit_26
                        $renpy.notify("Mental stress -1: "+ str(Mental))

            "Draw.":
                v "I think it's pretty important to take a step back and enjoy some more mundane hobbies, even during a time of such emotional distress such as exam week."
                v "Even though every part of my body wants to do something I consider productive..."
                v "...I can't deny that stopping to make a little drawing is therapeutic."
                v "After making a few doodles and a small finished sketch that I'm proud of, it's time to get back to work."
                $ Mental -= 1
                call minlimit from _call_minlimit_27
                $renpy.notify("Mental stress -1: "+ str(Mental))

            "No, just study.":
                v "Aww..."
                v "I guess it is the smart thing to do."
                v "I just really, really, really, really, really don't want to."
                v "Can you tell I don't want to study?"
                v "Really, really, really don't want to?"
                v "..."
                v "But I will."
                v "Because I'm a good student!"
                v "And a good student would never neglect her studies!"
                v "So I pull up the online science textbook, Visual Studio Code, the list of primary sources for history, and a French dictionary, and set off to unlock 110% of all my brainpower by studying all 4 subjects at once."
                v "It doesn't really do much but give me a headache..."
                v "But at least now no one can say I didn't try."
                
    label dinner:
        v "After a while, I get a message from my grandparents."
        $renpy.notify("grandma: when are you coming? food is ready")
        v "I guess that means it's finally time to stop studying!"
        v "Yay!!!!!"
        v "I make a mad dash for the door, grabbing my coat and my bag before quickly outpacing my parents to the car."
        v "Finally, we make the drive to my grandparents', and I gorge myself on their delicious cooking."
        v "I've been good today. I deserve it."
        v "We make small talk about school and clubs, but eventually it's time to go home."

    label endscene:
        scene bedroom light
        v "I spend the last few hours before bedtime messing around, treating myself to some real leisure time after a long school day."
        v "When the time comes, though..."
        v "...I open up a Google Sheet."
        v "My daily tracker Google Sheet, to be precise."
        v "I input the number of times I drank water today, my screen time, any money I spent..."
        if goodboypoints > 2:
            if not ban:
                v "As I'm about to fill in the last column, my phone starts buzzing incessantly."
                v "Grouchily, I turn back and check it, before I stifle a snicker."
                v "It's a text from my sister."
                show sistermsg 1 at truecenter
                v "Or rather, a series of texts."
                v "I can't help but laugh a little."
                v "Even after what I have to assume is a long day for the both of us, it seems I've yet to be forgotten."
                v "A lot of good things have happened today..."
                v "And I guess this was the cherry to top it all off."
                v "I shoot back a quick text, acknowledging her messages..." 
                show sistermsg 2 at truecenter
                v "...with a bit of levity of my own."
                v "Yeah, awesome-sauce sounds just about right for how cheesy I've been, huh..."
                v "It's been a good day."
                v "A really, really good day."
                v "If there's some god or otherwise higher power watching over me..."
                v "Making sure that everything went as nicely as it could..."
                v "I'm really grateful, okay?"
                v "Even if it was just one day of my life, days like this, that are so mundanely good to me..."
                v "They don't come around often, you know?"
                v "I find myself looking forward to tomorrow."

                v "With a smile, I turn off the light."
                scene bedroom dim
                v "It's been yet another lovely..."
                centered "{i}{size=+20}Day In The Life"

        elif Mental < 18 and Physical < 18 and Social < 18:
            if not ban:
                v "And finally, under the last column..."
                v "...I write, I had a good day today."
                v "With a smile, I turn off the light."
                scene bedroom dim
                v "It's been yet another lovely..."
                centered "{i}{size=+20}Day In The Life"
        else: 
            v "And finally, under the last column..."
            v "...I write, it wasn't a terrible day today, for once."
            v "With a smile, I turn off the light."
            scene bedroom dim
            v "It's been yet another lovely..."
            centered "{i}{size=+20}Day In The Life"
        return 

    label minlimit:
        if Physical < 0:
            $ Physical = 0
        if Mental < 0:
            $ Mental = 0
        if Social < 0:
            $ Social = 0
        return 