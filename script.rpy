## Everything that actually happens in-game is in this script file!
## Thus, everything in here was written by Valerie.

## Names of the characters who speak.
define v = Character("Valerie", who_color = "#ffffff")
define dad = Character("Dad")
define mom = Character("Mom")
define cm = Character("Classmate")
define c = Character("Mr. Cross", who_color = "#057536")
define w = Character("Mr. Wordley", who_color = "#7d490a")
define d = Character("Mr. Delva", who_color = "#752b5f")
define p = Character("Mme. Penny", who_color = "#476fff")

# todo list:
# credits for music on about page (done)
# credits for sound effects (done)
# edit save screen (halfway done - fix scroll bars and volume)
# change name colours to be visible (done)
# change quick menu
# change game icon (done)
# button click sound effects (done)

####

# 3 bad endings (stats > 100)
# 1 neutral ending (100>stats >= 50?)
# 1 good ending (stats < 50)

label start: 

    centered "Welcome to Valerie Simulator!"
    centered "Live through a day of Valerie's life, and make her decisions for her!"
    centered "Avoid increasing her {u}physical{/u}, {u}mental{/u}, and {u}social{/u} stress..."
    centered "Or else something bad might just happen!"
    centered "Have fun, and please enjoy..."
    $renpy.pause(delay = 0.75, hard = True)
    centered "{size=+20}{cps=*0.2} A Day In The Life"
    $renpy.pause(delay = 0.5, hard = True)

    stop music
    stop audio
    stop sound
    
    ## Variables to be used to set up flags for certain events, statuses, etc.
    $ late = False
    $ sick = False
    $ dressed = False
    $ dream = False
    $ hair = False
    $ food = False
    $ physicsq = False
    $ headache = False
    $ techflags = 0
    
    ## Fun little easter egg—if player wakes up late, morningtime will be set to a later time.
    $ morningtime = "6:30 AM"

    ## Used python's randint function to generate physical, mental, and social stress at the beginning of the game at a range of 1-20.
    ## Latechance gives the user a 50% chance of having the late status if they sleep in once.
    
    $ Physical = renpy.random.randint(1, 20)
    $ Mental = renpy.random.randint(1, 20)
    $ Social = renpy.random.randint(1, 20)
    $ latechance = renpy.random.randint(1, 10)

    ## Loops the alarm clock sound with a one-second fade in at 75% volume.
    play sound alarmclock loop fadein 1.0 volume 0.75
    scene black
    
    ## Neat little background transition. Fade and fadein are used to simulate the just-waking-up effect.
    scene bedroom dim
    with fade

    show screen my_notify(["Physical stress: " + str(Physical), "Mental stress: " + str(Mental), "Social stress: " + str(Social)])

    label dayone:
        "Be-be-be-beep!"
        "Be-be-be-beep!"

        v "{i}Ugh..."
        v "{i}What's that sound...?"
        v "{i}It's too early for this..."

        # Max: 23 mental, 25 physical; min: 3 mental, 0 physical
        ## Choice menu
        menu wakeup:
            "Get up.":
                $ Mental += 3
                $ Physical += -1 
                show screen my_notify(["Physical stress -1: " + str(Physical), "Mental stress +3: " + str(Mental)])
                jump awake 
            "Don't get up.":
                $ Mental += -1
                $ Physical += 1
                call minlimit
                show screen my_notify(["Physical stress +1: " + str(Physical), "Mental stress -1: " + str(Mental)])

                v "{cps=*0.5}...{/cps}"
                v "Zzz..."
                ".{w}.{w}."
                menu wakeup2:
                    "No, really, get up.":
                        $ Physical += -1
                        $ Mental += 4
                        show screen my_notify(["Physical stress -1: " + str(Physical), "Mental stress +4: " + str(Mental)])
                        call minlimit
                        if latechance % 2 == 0:
                            $ late = True

                            $ morningtime = "7:" + str(renpy.random.randint(20,40)) + " AM"
                        jump awake 
                    "Keep sleeping.":
                        stop sound
                        $ Mental += -2
                        $ Physical += 2
                        show screen my_notify(["Physical stress +2: " + str(Physical), "Mental stress -2: " + str(Mental)])
                        call minlimit
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
                call minlimit 
                v "I stare down the articles of clothing in my closet."
                v "Which will have the honour of being worn by me today?"
                v "\"Hmm... you!\"" with vpunch
                v "I snatch some clothes out, satisfied with my outfit coordination."
                $renpy.notify("Social stress -1: " + str(Social))
                v "Next, I'll..."
            jump morningroutine 
        
        label brushhair:
            $ hair = True
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
                
            $ coinflip = renpy.random.randint(2,3)

            v "I had a really weird dream last night."
            v "What was it about again...?"
            menu dreamchoices:
                "A death game.":
                    if coinflip % 2 == 1: 
                        $ Mental -= 10 
                        call minlimit
                    else:
                        $ Mental += 5
                    v "Oh yeah, that's right..."
                    v "There were 50 children on a hill who wouldn't behave while playing, and got punished as a result."
                    v "They were struck by a plague that caused them all to rip each other apart while they suffered internal bleeding."
                    v "I was the only one who got away, but I knew whoever created the sickness was watching me the whole time home."
                    v "Sounds ominous."
                    v "I'll write it down in my Google Sheet for dreams."
                    v "I think more people should write about their dreams. It's kinda fun to look back on what I was dreaming about a few months ago and wonder what my consciousness was up to."
                "A test.":
                    if coinflip % 2 == 1: 
                        $ Mental -= 10 
                        call minlimit
                    else:
                        $ Mental += 5
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
                    if coinflip % 2 == 1: 
                        $ Mental -= 10 
                        call minlimit
                    else:
                        $ Mental += 5
                    v "Mmm... yeah, that's right."
                    v "I think I was helping one of my classmates get together with someone?"
                    v "It felt like a fairytale-like environment, though."
                    v "Guess I was happy to third-wheel for the prince and princess."
                    v "Maybe I should read a little less rofan if it's starting to leak into my dreams..."
                    v "It's such an effective form of escapism, though."
                    v "I'll write it down in my Google Sheet for dreams, anyway."
                    v "I think more people should write about their dreams. It's kinda fun to look back on what I was dreaming about a few months ago and wonder what my consciousness was up to."
            $renpy.notify("Mental stress: " + str(Mental))
            jump morningroutine

        label eatfood:
            $ food = True
            $ Physical -= 2
            $renpy.notify("Physical stress -2: " + str(Physical))
            call minlimit
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

        scene car with fade

        v "The car ride to school is relatively uneventful. The radio provides background noise as I stare listlessly out the window."
        v "Maybe I should entertain myself?"

        menu carchoice:
            "Take my phone out.":
                $ Physical += 1
                $ Social -= 1
                show screen my_notify(["Physical stress +1: " + str(Physical), "Social stress -1: " + str(Social)])
                call minlimit
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
        
        scene school

        v "Finally, we arrive."

        if not late: 
            v "I've still got a bit of time to spare."
            v "Should I head to class right away, or...?"
            menu:
                "I'll go sit in the atrium with friends.":
                    $ Social -= 2
                    $renpy.notify("Social stress -2: " + str(Social))
                    call minlimit
                    scene atrium
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
                    show screen my_notify(["Social stress +1: " + str(Social), "Mental stress -1: " + str(Mental)])
                    call minlimit

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
        v "All the announcements end up on the {a=https://discord.gg/DAcWnXA7b9}{u}KSS Directory Discord server{/a}{/u}, so I'll just check there later."
        v "Nearing the end of the announcements, the class gets just slightly loud enough that I don't catch the joke of the day."
        v "Is it worth asking someone...?"
        menu joke:
            "Ask a classmate what the joke of the day was.":
                v "I tap on the shoulder of the girl sitting in front of me."
                v "\"Hey, what was the joke? I couldn't hear it.\""
                cm "\"What do you call a psychic little person who has escaped from prison? {p} A small medium at large.\""
                if Mental > 20:
                    $ Mental += -2
                    $renpy.notify("Mental stress -2: " + str(Mental))
                    call minlimit
                    v "\"...Heh.\""
                    v "You know what, that was pretty stupid."
                    v "Stupid enough to be funny."
                    c "\"Whaaaaat? That's so lame!\""
                    v "...Mr. Cross might disagree."
                    v "But he's wrong. That was a pretty awesome joke."
                    v "Good enough to make a bad day just a little better."
                else: 
                    $ Mental -= 1
                    $renpy.notify("Mental stress -1: " + str(Mental))
                    call minlimit 
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
        show cross
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
            show physicsproblem at center
            menu physics:
                c "{cps=0}\"If an object is placed between the focus and the centre of curvature of a concave mirror, what will its image look like?\""

                "The image will be bigger and upright.":
                    if not physicsq:
                        $ Social += 3
                        $ Mental += 3
                        show screen my_notify(["Social stress +3: " + str(Social), "Mental stress +3: " + str(Mental)])
                    c "\"Mmm... close, but not quite...\""
                    c "\"Can anyone else tell me the answer?\""
                    c "\"Sofia? How about you?\""
                    "Sofia" "\"The image will be larger and inverted.\""
                    v "I'd like to perish in my seat, if I could."
                    v "Someone somewhere around me answers the question correctly."
                    v "It's probably not that big of a deal, but that was pretty embarrassing."
                
                "The image will be bigger and inverted.":
                    $ Social -= 3
                    $ Mental -= 3
                    call minlimit
                    c "\"You got it!\""
                    show screen my_notify(["Social stress -3: " + str(Social), "Mental stress -3: " + str(Mental)])
                    c "\"See, guys, that wasn't that hard!\""
                    v "Speak for yourself, Mr. Cross."
                    v "My anxiety just spiked to an all-time high."

                "The image will be smaller and upright.":
                    if not physicsq:
                        $ Social += 4
                        $ Mental += 4
                        show screen my_notify(["Social stress +4: " + str(Social), "Mental stress +4: " + str(Mental)])
                    v "I can see my classmates giving each other confused glances all around me."
                    v "Wow, I guess I was really wrong."
                    v "Even Mr. Cross is looking at me like I'm a fascinating specimen with limited intelligent capacity."
                    v "Whoops."
    
                    c "\"Well...\""
                    c "\"You'd be right if it was opposite day!\""
                    c "\"The image will be larger and inverted, actually.\""
                    c "\"\'Good(?)\' guess, though...\""
                    v "Well, at least he's not ragging on me too much."
                    v "I just said the first thing that came to mind, anyway."

                "The image will be smaller and inverted.":
                    if not physicsq:
                        $ Social += 3
                        $ Mental += 3
                        show screen my_notify(["Social stress +3: " + str(Social), "Mental stress +3: " + str(Mental)])
                    c "\"Mmm... close, but not quite...\""
                    c "\"Can anyone else tell me the answer?\""
                    c "\"Sofia? How about you?\""
                    "Sofia" "\"The image will be larger and inverted.\""
                    v "I'd like to perish in my seat, if I could."
                    v "Someone somewhere around me answers the question correctly."
                    v "It's probably not that big of a deal, but that was pretty embarrassing."

                "I don't know...?" if not physicsq:
                    $ Social += 1
                    $ Mental += 1
                    show screen my_notify(["Social stress +1: " + str(Social), "Mental stress +1: " + str(Mental)])
                    $ physicsq = True
                    c "\"Well, why don't you give us a guess, anyway?\""
                    v "Darn. I was hoping he would take pity on me, but I guess I gotta give this a shot."
                    jump physics

        else:
            c "\"Sofia! You look like you know the answer! Why don't you give us a guess?\""
            $ Mental -= 2
            call minlimit
            v "Phew..."
            $renpy.notify("Mental stress -2: " + str(Mental))
            v "Glad it was someone else who was thrown under the bus."
            v "I bet in some alternate universe, I had to answer the question."
            v "It's a good thing it looks like Sofia knows what she's doing."
            "Sofia" "\"The image of the reflected object will be larger and inverted.\""
            c "\"Excellent!\""
            c "\"See, that wasn't that hard, was it?\""

        hide physicsproblem
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
                call minlimit
                v "At least I'm starting to feel a bit better, in terms of the stuffy nose and dry throat."
                $renpy.notify("Physical stress -1: " + str(Physical))
                v "I grab a drink of water, soothing my throat further."
                v "Seems like today is going better than usual in terms of recovering from my morning allergies."

    label historyclass:
        v "Finally, the bell rings to signal the end of class."
        v "Electing to not look at the whiteboard with tonight's homework scrawled on it, I head up the stairs to history class."
        scene classroom2
        v "I take my seat, noting that the desks have moved slightly since yesterday."
        v "\"These desks are so stupid...\""
        v "I don't know whose genius idea it was to make these absurd flower-petal shaped, asymmetric desks..."
        v "But I hope they're in severe pain right now."
        v "They're a pain to sit behind, they're a pain to move, they're a pain to put back in their original orientation..."
        v "They better be cheaper than the regular rectangular desks, because otherwise I can think of no rational reason why our school would choose to torture us with these desk models instead."
        
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
                            show wordley
                            v "\"Excuse me...\""
                            w "\"Yes?\""
                            v "\"I'm... not feeling great right now. I've messaged my parents to come pick me up, so could I go?\""
                            w "\"Oh yeah, sure. Just make sure to catch up on the work on the Minds Online.\""
                            v "\"Alright, thanks!\""
                            hide wordley
                            v "Phew. I head down to the atrium stairs, waiting for a reply from my father."
                            $renpy.pause(1.0)
                            $renpy.notify("Dad: ok coming in 20 mins")
                            v "Wearily, I let my head rest against the wall as I scroll on my phone."
                            v "Soon, my dad comes to pick me up."
                            scene car
                            v "At home, I can finally rest and recover."
                            v "It's okay to take a day off when I need it..."
                            scene bedroom dim
                            v "I'm gonna take a nap for now, though."
                            v "Goodnight..."
                            centered "Neutral Ending (Secret): Sick Day" with fade
                            return
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
        v "Mr. Wordley has a slideshow presentation open."
        v "I watch absent-mindedly as he clicks through slides, summing up the text and images before moving on to the next slide."
        v "Despite what just happened in science class, I find myself zoning out again."
        v "Thankfully, this time I don't have to worry about being called out for it."
        v "We make it through the presentation, then he gives us twenty minutes to work on the discussion question posted on Minds Online."
        v "Honestly, I don't want to do it, but it's not hard to write up something random that sounds smart enough to fly under the radar."
        v "I'll finish it up quickly, then spend the rest of class time daydreaming."
        v "\"Let's see... the discussion prompt is 'the pros and cons of having America as an ally'.\""
        v "Alright, that's not too hard."
        v "Given everything we've talked about in class..."

        $ historyanswer = renpy.input("What are the pros and cons of being allied with the United States?",length=100, multiline=True)
        if "military" or "trade" or "close" or "support" in historyanswer:
            $ Social -= 2
            call minlimit
            $renpy.notify("Social stress -2: " + str(Social))
        w "\"Let's look at some of your answers, huh?\""
        w "\"Valerie...\""
        w "\"'[historyanswer]...'\""
        w "\"Interesting point of view. I'll write a comment under your post.\""
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
        $renpy.notify("Physical stress -3: " + str(Physical))
        v "Yeah, I think I'll skip on my clubs today..."
        v "It's not like I can eat in the science lab, and I always forget to eat during math club."
        if sick:
            v "I have to get something in my stomach, anyway."
            v "Gotta stay energized if I want to keep making it through the day..."
        elif late:
            v "I barely got to eat anything for breakfast, so now is the time to compensate!"
        scene atrium with fade
        v "I'm the first to arrive in the atrium out of all my friends who eat there."
        v "I've always thought that that was weird. I mean, history class is on the third floor!"
        v "But it takes everyone upwards of five minutes to get here every day."
        v "Then again, maybe they have things to do other than come sit down on the crusty atrium steps to eat lunch..."
        v "Sad thought."
        v "Well, socializing in the halls right after class is pretty terrible in my opinion anyway."
        v "So many people..."
        v "Plus you have a 50% chance of accidentally bumping into someone at the stairwell while you're turning that corner!"
        v "Terrible design, really."
        v "Much like the atrium stairs. I mean, what even is going on there?"
        v "Your options are either to take giant steps or itty-bitty baby steps to get to the second floor."
        v "This is a hill I'm very willing to die on."
        v "I know I have friends who are willing to do so as well."
        v "Ah, speak of the devil..."
        v "\"Matthew, don't these stairs suck?\""
        v "I'm calling out to Matthew, who I can see taking pained steps up from the first floor to get to the step that I'm sitting on."
        v "Odd way to start a conversation, but I am nothing if not spontaneous."
        "Matthew" "\"(Generic Matthew Rant)\""
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
                    "Sofia" "\"Haha... I mean, it was okay...?\""
                    "Jessie" "\"Terrible. Horrible. I actually hated that.\""
                    v "Glad it wasn't me, then."
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
            v "Why am I here? Where is my computer??" with hpunch
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

    
    label scienceclub:
        $ Social -= 3
        $renpy.notify("Social stress -3: " + str(Social))
        v "Mhmm..."
        v "As part of the newly-formed Science Club exec team, it's my obligation to attend every meeting!"
        v "I would never ever dream of skipping out on it."
        v "I do have to check my phone to remember which room we're having our meeting in..."
        v "But that's all par for the course, and anyway I get there eventually."
        v "There, I greet my favourite Science Club president..."
        menu importantchoice:
            "Siya, of course!":
                v "Hi Siya!!!"
                v "You are so cool and awesome!!!"
                v "I love you so much."
            "Arzoi, naturally!":
                v "Hi Arzoi!!!"
                v "You are so cool and awesome!!!"
                v "I love you so much."
        v "I exchange greetings with everyone else too, of course."
        v "We might be a newly established club, but that just means that we're all very close with each other."
        v "Today's meeting is, as determined by popular vote, another GeoGuessr meeting!"
        v "I've never been very good at it, but I know many of our members are very, very competitive about it."
        v "I'm content to be Siya's sidekick again, like I am every time."
        v "Granted, it might be more appropriate to call myself her saboteur, considering how many times I've misled her from her original guess."
        v "It might be easier this time, though! For our warm-up session, we're just going over famous cities, so it can't be that hard."
        show geoguessr paris 
        $renpy.pause(2.0)
        menu paris:
            "Hmm, this looks like it's in..."

            "Asia.":
                v "Yeah, sounds about right."
                v "\"How about Asia?\""
                "Siya" "???"
                "Siya" "\"Okay Valerie, I trust you...\""
                "GeoGuessr" "Wrong! Paris!"

            "North America.":
                v "Yeah, sounds about right."
                v "\"How about North America?\""
                "Siya" "???"
                "Siya" "\"Okay Valerie, I trust you...\""
                "GeoGuessr" "Wrong! Paris!"

            "South America.":
                v "Yeah, sounds about right."
                v "\"How about South America?\""
                "Siya" "???"
                "Siya" "\"Okay Valerie, I trust you...\""
                "GeoGuessr" "Wrong! Paris!"

            "Australia":
                v "Yeah, sounds about right."
                v "\"How about Australia?\""
                "Siya" "???"
                "Siya" "\"Okay Valerie, I trust you...\""
                "GeoGuessr" "Wrong! Paris!"
            
            "Europe":
                v "Yeah, sounds about right."
                v "\"How about Europe?\""
                "Siya" "Hmm..."
                "Siya" "\"Okay Valerie, I trust you...\""
                "Siya" "\"Where in Europe?\""
                menu paris:
                    "France":
                        "Siya" "\"Sounds reasonable...\""
                        "Siya" "\"Where in France?\""
                        

            "Africa":






    label mathclub:
        $ Mental -= 3
        $renpy.notify("Mental stress -3: " + str(Mental))

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
        v "And so I spend my entire tech period in the library, painstakingly tweaking away at text and adding graphics features that I didn't really need and that don't add to the technical aspect of the game."
        v "It might not get me a good mark, but it makes me happy and that's what matters."
        v "Next period is tech anyway, so I'm getting a decent head start on that."
        v "I know there's a particular classmate of mine who disapproves of me spending all my time on the graphics..."
        v "And while he might have a point there, I want to work on what I enjoy!"
        v "So I work away until the bell rings, content with the progress I've made."
        
        jump techclassgood

    
    label nap:
        $ Mental -=5
        $ Physical -= 5
        $ Social += 5
        show screen my_notify(["Social stress +5: " + str(Social), "Mental stress -5: " + str(Mental), "Physical stress -5: " + str(Physical)])
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
        scene library with Fade(0.5,1.5,0.5)
        v "I wake up before the bell, much to my disgust."
        v "My phone is vibrating like crazy next to me. I have half a mind to disregard it, but..."
        if late:
            v "This morning has taught me that, when in doubt, I should check the time before going back to sleep."
        v "I guess if there's something urgent going on, I should check, right?"
        v "...Ah."
        show phone 
        v "I have 6 missed calls from 4 different people, and my phone is currently ringing."
        v "Blearily, I blink until my vision clears."
        v "\"Ah.\""
        v "The time is 11:50. I have even more missed texts."
        show screen my_notify(["where r u", "where r u", "where r u", "???", "class is in 5 mins"])
        v "Oops."
        v "Guess I didn't tell anyone where I was going for lunch period, huh?"
        v "It's probably fine. It's not like I'm late."
        v "...Yet."
        v "...Anyway, Mr. Delva probably doesn't care. It's fine!"
        v "Still, I hurriedly throw my things into my bag, not bothering to zip it up before I dash out of the library."
        v "Hopefully I didn't leave anything behind."

        

    label techclassgood:
        v ""

    label techclassneutral:

    label techclassbad:
                    



    label minlimit:
        if Physical < 0:
            $ Physical = 0
        if Mental < 0:
            $ Mental = 0
        if Social < 0:
            $ Social = 0
        return 
        
        

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
