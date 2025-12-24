Meeting Title: QA: Getting AI Agents to Production
Date: Nov 25
Meeting participants: Fabian Melendez, Daniel Wessel, Andre Lubbe

Transcript:
 
Me: Hello? Guys, if you're all on the same project, if you have different projects with LLMs, if you have multiple tools and multiple whatever or multiple problems just like skipping and then just, like yeah. Just mention it. Okay? Because it might be you have to work with different tool stacks for different yeah, suppliers, you know, like you're working for. Vendors. Okay. So first of all, basically, my first question is what frameworks you're using? Actively and yeah. And and maybe also why, but it's not that important.  
Them: What what do you mean by frameworks?  
Me: Like AI agent frameworks. Oh, sorry. The whole thing is about AI in this case. Right? So LLMs, how you use LLMs and which frameworks tool etcetera, you use for them. Yep.  
Them: Okay.  
Me: So  
Them: Nice little  
Me: So  
Them: Go ahead. I can start. For me, in one project, we're using just directly the APIs from whatever. Model we wanna work with plus then light LLM. Sometimes. Is just a wrapper around all the the models. But nothing on them, like, the orchestration side. We go to own orchestration stuff. Another project we use ADK, so the Google app sorry, agent developer kit.  
Me: Yes.  
Them: Yeah.  
Me: Okay. Fabian, the the same for you.  
Them: I mean, sort of. I mean, we're using OpenAI We're also using NovaSonic from Amazon.  
Me: Okay.  
Them: We're also using Gemini. And we built kind of some blue code to be able to call all of them kind of on the same interface. Besides from that, we used a little bit the agents SDK from OpenAI, but as frameworks themselves, I would say mostly we were using the raw APIs from all of these companies which are massively different.  
Me: Okay.  
Them: Massively. They're the same, they implemented very differently.  
Me: Okay. So you never came across lang lang graph, lang chain, like,  
Them: I  
Me: crew AI, any of any of them other than agent SDK from Google?  
Them: I mean, I I've seen those I just never convinced because whatever new stuff comes comes out in the API, language chain is slightly below, like, just not update and, like, fast enough for me to try this out quickly. So that's why we did this, and we were trying some stuff that we didn't find like, a LAN chain interface that would do this. So for example, for structure output, although it's just, like, maybe a spin off of function calling, we didn't find this in Limechain. So it was easier to just use the raw APIs and just build ourselves the the code to call it.  
Me: Okay.  
Them: I can say that we also, like, use a little bit of lane chain and, like, some isolated thing, the lang graph we played around with to see if we could rewrite what we have in lang graph. But it wasn't worth the effort to kinda take everything because there was quite a lot that was already there when we first came into it.  
Me: Okay. We'll share our insights later. Right? So you'll get at the end when I stop the recording, Burak can then go and steam off everything. He also experienced Then, like, how you evaluate like, and how you test? What tools do you use there? Do you have any, like, things you look at in that point? Like,  
Them: We're using langfuse for at least tracing and then keeping track of the evaluation performance.  
Me: Okay.  
Them: We were using we were using LangSmith before, and we swapped over to LangFuse  
Me: And you use it  
Them: because you could do your own self deploy.  
Me: Okay.  
Them: Ah, but is that the only reason?  
Me: And then  
Them: Also cost. Yeah. But okay. If you weren't paying for it, which one would you pick? Just from experience wise, I felt as though maybe Lang Smith was a bit nicer. But to be honest, they're both kinda similar.  
Me: Okay. And  
Them: Yeah. I see.  
Me: and for evaluations, what do you use? How because you mentioned that in length length fuse, do the evaluations as well.  
Them: We just write so we use the built in datasets  
Me: You use the built in.  
Them: that they have, and then we do the evaluation on our side. Either use an LLM as a judge or not. And then write it back. But there's no no tools that we're using for that specifically. It's kinda prebuilt. You're using some sort of g, Evan? What's the metric? It depends on if it's evaluating tool calling. It's just to see, okay, are the the is the right tool called? Is the right set of parameters set with the right values? Or having a element as a judge to determine if things are roughly the same as what we would expect. Right? If you say open window, right, that could be 5%. That could be 10%. But you don't wanna enumerate every value. It just let the LLM decide for you. But then in other cases, we have higher level, evaluations that have been built that look at very specific KPIs. Like, does it stay on topic to what the user asks Does it actually accomplish what the user asked? Does it stick to certain policies? Like, there's a bunch of different things that we have. Yeah. Okay. So you're doing more of a yes and no checks and no scoring. Right? Because I was gonna ask you you keep this score. This is a little bit. Because they fluctuate. Right? Like, there could be different levels of the score where, like, okay, it partially meets it versus if fully meets it, but that is then done to match human labels in a way. So the the human labels, set the ground truth. You then check to see if your LLM judge is able to come up with something similar to the human labels. And then you use that. K. Maybe let me ask another Let's say you have one output. You evaluate it a thousand times. Do you get the same score every time? That's what I'm asking. No. We don't. Yeah. Okay. But that's that's because either because the the same output isn't always evaluated the same way or because it doesn't always output the same output. Right? Either you have the non determinism on the model side or on the evaluator side. Yeah. Yeah. So imagine I have one output. You know? It's static there. But I evaluate one times, and then you tell me, hey. Some scores are not you know, it's just out of place. And this is normal. Again, I'm asking because the reliable scoring is still a problem. Right? Yeah. Because of the nondeterminism in the model that you use for your evaluator. Yeah. I really didn't have this  
Me: Okay.  
Them: I mean, we also did unit testing to just make sure that API spits out what it says it's gonna do and, like, function colon has you know, proper parameters but we didn't need anything beyond that so far. Because most of prototypes I mean, there are assortable tests. Right?  
Me: Okay.  
Them: If you're picking labels, etcetera, it's like a selection, you have the expected output. But there are cases it's not like this. You know? I mean, we have, like, refund flows, etcetera. On the platform, and there it has to evaluate how did I make this classification.  
Me: Okay. Let's continue. The so the next question would be around like you're collecting all the traces, Daniel, right? You mentioned you used Language for this. What you do with that data? Is there anything else other than, like, you're looking at evaluations?  
Them: So we can use it to generate new data points in the dataset. We don't really do that. We it's more just  
Me: Okay.  
Them: if you're debugging most of the time right now, that's what we're using it for.  
Me: So you use it for debugging. And you mentioned before we continue, it's like you switch frameworks on the on the free stack. Right? But did you also switch on the model side? Or do you have to  
Them: No. It's it's mostly been focused around OpenAI.  
Me: Okay. Any reason for this?  
Them: That was just That was just the one that came out with the the real time models before everyone else did.  
Me: Okay.  
Them: Like, the speech to speech stuff.  
Me: So you're using it because of speech? Because you have a speech use case.  
Them: Yep.  
Me: Okay. And how you manage your your keys? Is it, like, how is that done with  
Them: For the tech  
Me: within your project environment?  
Them: For the text based stuff, it's all bricks o l m. But for the speech to speech, since Bricks LLM doesn't support, at least the version that we're using doesn't support speech to speech API, like the real time API. We have to go directly to the to whatever hosting if it's Azure or OpenAI.  
Me: Okay. Okay. Cool. Then that was the first block kind of The the second was now, like, would like to learn about the I mean, if Purag already dived into it a a bit, like, how you optimize, like, basically, the system, your workflow, the application. So, if you could just walk us through a bit of how you like yeah, optimize the agent's performance, the orchestrator, whatever your system looks like. And, yeah, how you how you how you went along basically building it.  
Them: In theory or in practice?  
Me: No. How you actually did it? I'm not interested in theory because we all wanna build something  
Them: Yeah. I mean, in theory, we should be using our evaluations as a guide for then how we change it. We don't. It's more, vibe based, when we're sitting in the the like, interacting with the system directly. If it makes sense to change things or not. That's kind of it's a lot of manual testing right now and just kind of direction of what feels like it's doing better than before. But in theory, we should be using the evaluations a lot more as the the theoretical foundation for why we're making the changes.  
Me: Okay. And so you do an AP test. You adjust the prompts, and you run a certain set again, or how do you do that?  
Them: Like I said, we don't even like, it's you just run through a certain use case or set of use cases and see if it works better. But we don't have, like, the data points  
Me: Okay.  
Them: We're not running against the data points and checking the evaluations. So often.  
Me: Okay. Is the same for you, Fabian?  
Them: Yeah. I would say so. I mean, we pretty much what I do is I enabled UX person that will look at the experience.  
Me: Okay.  
Them: And just the person goes through several demos and figures out what needs to be changed and tries it very holistically.  
Me: Okay. Basically, let, like, a third per like, a second person look at the results, but not in a structured way more like in a pay, try it out way.  
Them: Yep.  
Me: Okay. But so there is the a cut UX side to it where you okay. That that's good to know. And then there's, like, so now when you identify an agent under perform, so you're finding, like, problems either problems, whatever problems you have, and you also explain with the problems you have. How the how do you identify why it's underperforming and how you go about doing, like, your yeah. Your your root cause analysis, I would say.  
Them: Should I go? Or  
Me: Don't feel ashamed of anything you say. Right? Like, it's not that we have been so different. Like,  
Them: I mean,  
Me: there's always the best version of doing it.  
Them: underperforming  
Me: Yeah.  
Them: could come in two ways. One could be like, latency. And for that,  
Me: Okay.  
Them: I mean, we tried a few things, mostly going out to a APIs or real time, for example, or trying to optimize different parts of the system. But kind of have to deal with what you have. So there's not a lot that we can optimize there from, like, quality of whatever we're getting out. I would say it's kind of, like, tied to the last answer where the problem is we already know what we want to get out of the LLM, at least in in terms of, like, how complete should it be, how expensive should it be, and then we just adapt the prompt until we get that rolling. But talking about very short lived demos in my case, so it's easy to do that We're not building, like, this one system to rule them all or something. So  
Me: Okay. Then maybe we ask Daniel first, and then I'll hypothetically ask you what you would do if you would now have to bring it live for 1,000,000. Conversations.  
Them: Okay. Yeah. I mean, use the tracing tools that we have both the logs for the the system we have deployed plus then the tracing on link views to try and figure out what is happening, which tools are potentially being called incorrectly, or, what And then that kind of dictates where we should look if it's on the prompt inside, such as the tool description or whatever, or if we see that maybe there's some extra information that's missing, Yeah. That kind of stuff.  
Me: Okay. So Did you ever get to the point where you felt like you'd you can't fix it? You're like, right. And why?  
Them: We just try some different approach, I think, in that case. Like, we we have a theory. We test that theory. If it doesn't work, try a different approach. Like, there is no in my opinion, there's no, like, perfect solution that will fit every single use case. Right? So you have to kinda figure out, okay, what is another way that we could do this, see if someone else is doing something similar,  
Me: Okay, so you tried  
Them: whatever.  
Me: Okay. So you try to turn a few knobs and see like that across all the test case, it kind of stays and kind of a poor gut feeling wise it doesn't drop somewhere, on some test data set points or how do I should I understand this answer?  
Them: Like, say we have a theory of how to I don't know. Inject some information into the the model. Right?  
Me: Yes.  
Them: That way, uses some certain context to answer a question better. There's a thousand ways you can do that. We have an idea of which one we think it will work. We try to inject it that way. If it doesn't, work in the way that we want it to work, then go back and try a different way. It's not that we spend a lot of time trying to make one specific way work because we know that it's possible that it will work given the amount of time, but it's also possible that it's never will because of the model capabilities that we're working with.  
Me: Okay. If you say, like, not to put the amount of time, like, how much time you spend on all of this like, bug fixing root cause, all of that stuff. How much part of your work of your time yeah, is it actually?  
Them: Good question. I'd say that you can get like, a working implementation rather quickly, but then a majority of your time is fixing those small issues. Right? And that's where you didn't have to figure out the cause as to why is it not working in this case versus that case and those things. So, yeah, I'd say maybe half my time on that.  
Me: Okay. Does this back your experience, Fabian?  
Them: I'm I'm not sure. Like, good generic to to kind of fit it to something. Like, to your previous question, like, we couldn't fix something. Maybe I can frame it another way. Did you have to put a warning saying that time spent adjusting this prompt? Or not ever. I mean, that that's where I I kind of just give that to our UX person, and I just don't deal with something that much. And I deal most with the system.  
Me: Okay.  
Them: I would say she would spend probably a full day on this every month or so depending how often we have to adjust new  
Me: Okay.  
Them: content. But Sorry. How often do you readjust if you have new edge cases? So that that's it. Like, when we introduce new functionality usually, like, it depends a lot on what we're doing. We had this quite a lot that we had to test different prompting on different systems. So if we were using NovaSonic and we were using OpenAI, sometimes you had to be more explicit on some stuff in one of the two systems. And she would spend some time just of getting roughly the same experience out of them, whatever we were trying to optimize. Yeah.  
Me: Okay.  
Them: May one more question. What's the ratio of the agents versus prompt chains? Right? So certain features are, like, state machines. It's, like, bunch of prompts chain together, but then you also have standalone agents. In our project, this was like, the prompt was the smallest part of our system just because we were trying to orchestrate a lot of things. We were trying to put animations next to things, and that meant moving a lot with timings and, like, introducing messages, popping out in the middle of like, some API calls and stuff like that. So it was mostly on, like, not the prompting side as much as the system itself and, like, whatever. Were using for. In one project, we have probably half and half of some things. It's just a bunch of pumps changed back to back. Some things are agents that you interact with or do stuff. The other project is almost purely agents, and there's only one prompt chain. Do some extraction of some stuff.  
Me: Okay. Makes sense. Let's talk about the so let's finish that, like, testing optimization patch. So the next one is more about release. I guess you all can think about already where this is going, but how do you feel about yeah, when you now made the changes and you have to release it? How do you how do you go about this? And, yeah, like, run me through the process that your feelings and how you do it when you go to production.  
Them: Production is a big word for what I've been doing. So releasing it in a way, it's mostly an orchestrated set of pipelines that I have.  
Me: Yeah.  
Them: So there's nothing much other than that. The system can also go down if needed to adjust it.  
Me: Okay.  
Them: So  
Me: Okay.  
Them: mostly self built infrastructure to do this.  
Me: Okay. Any any specific release process you follow, any tests you do,  
Them: There are let's say, set of they're kind of unit tests, but with LLMs, like, it's difficult to have that concept, but we do run that as a regression just to make sure that we didn't break the API calling  
Me: Mhmm.  
Them: But that all happens in the pipeline, and it's also not that time consuming or that intense. So not really that way. Maybe the other guys have done a lot more on that. It's just a Kubernetes stuff that deploys.  
Me: Okay.  
Them: For us, whenever we merge in a new feature, we go  
Me: Okay.  
Them: through and check all the use cases that we normally want to support. And check for a regression on them, and that's basically it.  
Me: You use the test data set in length use for it, and you just run it on the latest prompt  
Them: That is that is one way, and then the other way is just  
Me: Okay. So you do it manually kind of  
Them: sitting and interacting with it for, like, five, ten minutes.  
Me: Okay. So you do it manually kind of. You have your playbook in.  
Them: Both. Both.  
Me: Okay.  
Them: Yeah. We we usually still manually test because we need to see it working. So  
Me: Okay. Yeah. And just from a personal feeling, like, have you ever when did you ever feel like this was stressing you out because of the pure frickleness of LLMs and whatsoever? Or never got to that point where this, like, really, like, was an issue.  
Them: Not not pretty work, but I it's like something you have to do. Right? Like, at the end, there's something that will present to a client. So have to also have the the peace of mind that does behave like you expected and that you can see it working and I don't know, make a video out of it or whatever. So, yeah, you can also have some proof.  
Me: Okay.  
Them: But On as a necessary annoyment thing, like, you just have to Well, if you're client hands you out a dataset that's a thousand items. Right? And it says this needs to work. Mhmm. I've haven't been on that scenario. I mean, we would do is, like, probably automated testing like we've done, but I guess we will rebuild a lot of but in our experience, these systems are barely being created. So we're going through that list of items, and it's never been, like, like, we actually have to take this out of the client so that we have enough use cases for the the system to be meaningful.  
Me: Yeah. Okay. Daniel, for you, I guess, for the bigger projects, I guess there's some other  
Them: I mean, they never really said, hey. These all need to work. Right?  
Me: Okay.  
Them: It's mostly about happy path. Right now. And stuff. So  
Me: So the client naturally understands that this is, like, a fickle system, and it won't get you, like, 100% or something on on all of that.  
Them: On the stuff that I've worked on, right, in other projects at Moshe's, definitely there's cases where the client's like, hey, why isn't this working this very specific situation? And, yeah, it's a bit more annoying, but in the that I've worked on, they're a lot more lenient as long as the the main paths are working.  
Me: Okay. Now I ask Andre. As from the product side. How do you feel prior to releases and of these kind of systems?  
Them: I feel prior to releases of the system  
Me: Yeah. Of these chat systems, agent systems, systems, other lens because as, like, a product person,  
Them: I mean, due to the  
Me: Let me ask you a bit differently. You know, with traditional software, you just  
Them: yeah.  
Me: just you do real, like, you do your test, your unit test, all of that stuff. You test your releases. You make the release candidate. Then you press the button. You deploy it to production. You're kind of very confident it works. Right? Because you kind of, over the time, grew your test set and bench and everything. And  
Them: Yeah.  
Me: you can test for regression. We've probably and LLMs and different models, models changing. Prompts changing everything. It it's different. Right? So how that's my question. How do you feel in this kind of scenario of  
Them: Sure.  
Me: deploying AI?  
Them: I mean, I can I won't say release, but rather we see those those very big demos as our releases kind of, right,  
Me: Yep.  
Them: For us in the predevelopment, this is the the the big release? Compared to stuff that we've done in the past where you release it, then it's finished and it works. Yeah. This is pretty stressy, I must say, because leading up to it, I can I I just also tapped the vibe of the whole team leading up to it There's, like, a ton of stuff that that's still, like, a gamble, the the prompts? It can still go wrong at at any moment. Right? So we have, like, this often this wizard of us kind of control over it that you can quickly get it back on track when it goes off the rails. So the releases work very differently. It's not like a fire and forget type of thing. It will never be released. Kind of. You know what I mean? In the in the one point zero state,  
Me: Yes.  
Them: Yeah.  
Me: It's more continuous all the time. Right?  
Them: Yeah. Exactly. And people don't understand that, that because they still compare it with conventional software They think you deliver it, then it's over. But in this case, it's it's really not because the models change all the time. So then all of the, tasting has to keep on going. Going. The the, like, quality KPI stuff you can never ever stop as long as they will bring out new models.  
Me: Okay. Anything you  
Them: The ones they have?  
Me: Sorry. Yes?  
Them: Oh, the one thing I would add is the one of the annoying parts is guardrailing, which you know, it is the only part that people would look at so that stuff that does does doesn't get said. Like, not calling a function, Man. So so hiccup in the system. No one really cares, but a system outputting something that you never wanted to be output, that's the that is the one thing that I that just takes a bit off time, and it's still not a 100% safe for how how do you do this. So guardrailing is the one corporate interest where you still have to, like, think about this.  
Me: Okay. That's that's an important point, Burak. Yeah.  
Them: And it's it's  
Me: Yeah.  
Them: and this is  
Me: Yep.  
Them: right. Because there's legal liabilities. Right? So that's  
Me: Yep. Yeah. Makes a lot of sense.  
Them: that's why or even on, like, simple stuff, like, people still ask about this even if you tell them this will never hit the client, they were still like, but yeah. But how would we do it? That's still over there quite a lot.  
Me: Okay. Daniel, anything to add?  
Them: I think the covering is a good point. No problem.  
Me: Okay. I have a few more questions, but then then we touched this kind of already. Because you already talked about maintaining agents then and all of that stuff. Okay. May maybe talk about this for a How you do it with budget and and procurement, Andre? So how does it work? I guess you have your API keys. From the supplier in your case, or how how do you do it?  
Them: Yeah. In in some it's different for every project. In some projects, we have to have all of it, and we invoice them as story points.  
Me: Okay.  
Them: For the usage of AI. And then in others, we reuse what they have have. And then we don't care about usage limits.  
Me: Okay.  
Them: So in big enough projects, it's like that. But in other projects, custom partners have told us, hey. We have no way for us to give you, like, this key. Just use it and make it, like, hours that you're invoicing us.  
Me: And if you would need new tooling, like, assuming there would be a new cool tool, like, on top which would support you on the pains we just discussed. How would that work like?  
Them: Depends on if it's a tool the customer has to know about. So I directly compare Daniel and Fabian here. In Daniel's case, I feel like there's a whole team rather hands on.  
Me: Yeah.  
Them: In in his ecosystem. They would care about it, and you need to sell it to them. In Fabian's case, Fabian and jump in if if I I don't wanna speak for you guys, but in Fabian's case, if he up one morning and has the idea of using something, and it works, and it makes his life easy, nothing, is gonna stand in his way as long as it's not like fucking enabling Russian hackers to to steal cars.  
Me: He'll take your credit card and just buy the subscription.  
Them: Exactly like that. But in Daniel's case, there's sadly a little more scrutiny. I also but I think Daniel is in the fortunate position of having complete technical leadership there so he can  
Me: Okay.  
Them: shoulder his way in. But nonetheless, there's scrutiny because people around him know a lot  
Me: So let's ask again, Daniel. You said you had lengthsmiths and then you went to Lang's Fuse also because of cost. How was how did you buy Lang Smith before  
Them: as well.  
Me: or was it just an Azure service you bought?  
Them: That was bought by the partner.  
Me: That was part by the partner.  
Them: So they had a partnership. That's why they started using it. Also, why they stopped using it because they didn't extend the partnership.  
Me: Okay. So it came by a different vendor.  
Them: I  
Me: Basically.  
Them: based on not current projects but past projects, this also is mostly massively influenced at what they already have in their clouds or they can  
Me: Okay.  
Them: easily enable as a corporate. So if it's a customer that's using Google, and then it's part of whatever Vertex AI offers or is part of a marketplace thing that they can do. They'll do it. In this case, I feel like compliance is the main thing they're looking at. Like, sometimes the price will not be as important because they will rather run, like, you know, the the models on Azure directly than having to evaluate the whole system to see if it's compliant to their privacy stuff because it's customer data. So there, I feel like the price hasn't been as impact compliance that they already have in their corporate.  
Me: Okay.  
Them: White listing.  
Me: Okay. Thanks. So now the last one is basically we talked about few pain points now, and like, approved problems. I mean, you you got the questions I was asking. It was around, like, bringing agent to production of continents and how you get agent lives and how you maintain them in production. How you make sure changes don't break the system, etcetera. Which would be the features that would help you most in your day to day work. Thinking about everything we just discussed. Something you don't have maybe or something you would like  
Them: Naked  
Me: to see in tool in the tool stack you already have.  
Them: I think making it easier or more integrated to do this kind of evaluations like, running these this test suite. So that way, instead of it being vibe driven, it's actually okay. We we do this. We run the the test data points. And get the hard numbers we can see the difference in the two approaches. That would at least guide the work I do in a more data driven approach But, obviously, that's money and time that you have to wait for in between every single run of these. Right? Because the run could take thirty minutes. It could cost  
Me: Mhmm.  
Them: a $100, whatever. Right?  
Me: And if you say, like, you can't I mean, you kind of can do this already if you want to, but is it the interface you're getting because it's kind of in a UI and it's not bound to, like, in a CICD, or you can't put it into, like, a some kind of testing environment. How would how would you like to see this?  
Them: I think it's about adding I think the reason why I don't use it so much is when I'm adding new feature, I don't have, like, a full dataset of all the tests that I want. And  
Me: Okay.  
Them: a easy way to add new data points into this we ended up building, like, something that uses, an LM to then come up with alternatives for a data point. Like, you have a data like, a situation that you tested,  
Me: Yes.  
Them: You say, hey. I like this one. Give me five examples that are very similar to this. And then that works in kind of building up this stuff, but, like, the process of bootstrapping this dataset is a pain sometimes, so it just doesn't happen. Then it ends up coming down to you doing this based off of  
Me: Okay.  
Them: how it feels to you.  
Me: Anything you wanna add, Fabian?  
Them: No. I mean, I I do think that a tool that tackles that would make it easier. But as like, there's a fine line at least in my line of work of how much of how simple it is, like, how bloated does my thing gets.  
Me: Mhmm.  
Them: Versus how much I get out of it. And that's the power even if you offer me right now, I will still be hesitant because it's like I have to come up with all the test cases right now because I don't have them for my client, as Daniel said. For a rollout system, like, if you're really thinking about  
Me: Okay.  
Them: long term, that makes sense.  
Me: Okay.  
Them: And I would probably start looking there when I start building my system from scratch, like, okay. I think I'm gonna need this so that I can have enough data so I can evaluate what  
Me: Yeah.  
Them: are experiencing and so on. But haven't been there.  
Me: I mean, we can talk about our solution now a bit, I guess. So we are targeting basically teams that are in this stage of, like, hey. I built v one of the product, and I'm enrolling it out to the public, and I'm starting to collect production data. So you kind of get a big, big chunk of data, like, in best case, a 100,000 of conversations or flows or whatsoever. And then you kind of get swamped by data in this case, and then you cannot manually go through each of them anymore. So this is, where we kind of wanna go with our solution. And then, obviously, it it should our tool, our feature should have two things. First one would be like, getting insights, like, basically, automatically getting insights on how good your system works based on your evaluations, maybe additionally with our our set of evaluations, whatever we have. So we didn't define this yet. And then the second thing is directly getting recommendations and the optimization. So kind of maybe, Daniel, know it as DSPY. So kind of in a prompt mutator, which then tells you, look, you have to improve your your prompt from the agent or you're just your single prompt chain. You have to improve your descriptions of your tools. Whatever. So kind of this kind of optimization schema, and then obviously show you before and after. So this is kind of where we wanna go. So not only saying like, hey. You should try this. But also show you, like, you can do these tests and say, hey. If I make these changes, this is across the board how my whole use case performs. But, obviously, it comes as Fabian you said with a dataset. And good evaluation or, like, a labeled dataset, I would say.  
Them: Mhmm.  
Me: Borek, any you took some notes now. You probably have some further questions. Right?  
Them: I mean, I tried to ask them in the meantime.  
Me: Yeah.  
Them: But, yeah, no. I think I got most of my questions answered.  
Me: Okay. What do you think about this kind of solution, Daniel? You haven't said anything. Like, would would this help you?  
Them: I mean, I think having something like that, if you can take the time to set up your system to work with something like that, it definitely helps. I mean, I've experimented a bit with getting, like, I don't know, Claude or or or whatever to rewrite my prompts. Also, given the the prompting guides for whatever model I'm using, Kind of mixed results. Sometimes it works better. Sometimes it doesn't. I think it's a lot harder when you then start working with speech. Right? Because with speech, There's a lot of things that you can't just, like, have a evaluation kinda just set up for. Right? Like, unless you have a very complex evaluations that look at, okay, the the accent of the of the voice or the how clear it speaks or those types of things where it's very hard to to get actual KPIs and numbers for that to then see a difference between the two. Then that's where such a system may fall apart. Like, text wise, yes, super easy to to set up this stuff. It's kind of clear that this is something that would make sense. But once you then also include the speech, modality, then it becomes a lot more difficult, I think.  
Me: So so we would we would need different scores or inbox for this. Right? So you would be able to bring your own analysis, kind of your own  
Them: Yeah.  
Me: I this is your set or this is what you use from whatever you have, but please also in your scoring evaluation when you optimize  
Them: Yeah. I mean,  
Me: use this  
Them: that would then require whoever is to build those things. And, obviously, it's a good thing to have those things, but especially when it comes to the the audio or the speech modality, it becomes a lot more difficult than a text based system to build this stuff.  
Me: Yes. I understand. Now I feel like time traveling back to sitting in beta left.  
Them: By the way, how much of your code is generated versus written at this What's your, like, day to day coding setup these days? It's depends on how you describe generated if you describe the the tab complete for when you're writing and it's using Yeah. Like, title suggestions. Flat out generate stuff with cloud code after planning? Yeah. Sometimes. Yeah. Okay. Sometimes I've let it As it works? Sometimes I use it Yeah. Normally, it will work if I want to do something quickly. But then, obviously, if I want to then bring that into something that using for production, 