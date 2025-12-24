Meeting Title: Bene x LunaLift (AI Agents to Production)
Date: Nov 26
Meeting participants: Johannes

Transcript:
 
Them: Fast workflow that can handle like, your data processing without a lot of waste.  
Me: Okay.  
Them: So and and, basically, more like the newbies, I would say, they were to solve everything with LLMs even where it's not the right tool for the job.  
Me: Okay.  
Them: At all. And so I would say that where we sit. Like so I actually didn't work out too keep the answer shortcut.  
Me: It's fine. You you're already browsing most of there's other questions coming, but you already answered them. So I'm gonna skip them later on. That's good.  
Them: Mhmm. Yeah.  
Me: This Can I follow-up on one thing on the text text? So you use anything  
Them: Mhmm.  
Me: evaluation and testing. So any DLLM codes you're making, you use anything like deep eval, composer, g eval. You use anything like length use, lengthness to look at traces and data. What  
Them: No. That's actually also like, we we use, like, open telemetry kind of classic  
Me: Okay.  
Them: stack that we also use for monitoring your our yeah, our AI driven, like, flows  
Me: Okay.  
Them: And we so far, we because we already have our adapters where we pass out the usage  
Me: Yes.  
Them: So I would say, like, from what I've seen, the only two things specific to AI kind of observability currently required where where, like, token usage usage and speed and and maybe, like, GPU, TPU specific,  
Me: Okay.  
Them: kind of metrics on the machine usage.  
Me: Okay.  
Them: I mean, in in the, like, DevOps sense, I think there is obvious like, a lot more, m ops when you have, like, kind of online model training, etcetera, where you can go  
Me: Okay.  
Them: a lot deeper. But, we we have plans for having some online, learning.  
Me: Okay.  
Them: In in the in the flow, but we haven't implemented that yet.  
Me: Okay. And how you manage your prompts? You haven't when you have prompts, or you solely work on models?  
Them: And so, actually, those are they're actually, in a in a normal post Postgres timescale DB.  
Me: Okay.  
Them: Where we monitor the performance also manually, actually. Yeah.  
Me: Okay. Okay. Well, that's fine. Okay. This is why we're looking at it. This is why I asked the questions. What you say kind of is very in line with all the other interviews I had so far.  
Them: Okay.  
Me: I was expecting it to be completely different, but yeah. So like, specifically looking at prompts and how you manage the prompt. And you say, you would do it manually. Can you work me on your work me walk me through your optimization workflow? So, like, how do you test changes of prompt, system instructions of agents, Do you have a test dataset? Do you do a b testing before after? Like, how do you kind of go on making changes within that? Specific sections of, like, where you change prompts, agents, etcetera?  
Them: Mhmm.  
Me: Not your overall system, but specifically around AI agents and LLM prompts.  
Them: Why it's Right. Okay. Yeah. I have to say, like, actually, in terms of instructions is a bit like, manual try and try and error, to be fair. Like, it's actually  
Me: Okay.  
Them: just checking, okay, what gives the like, most, like, feasible results for now. We also don't like I would say there, it is actually a bit different. What what kind of problems we talk about because we are we do, like, a lot of prompt monitoring for our customers.  
Me: Okay.  
Them: Where they want to see how does the company show up in terms that their customers might  
Me: Yes.  
Them: come to the l and m. So it's not that it's not necessary. Necessarily like an optimization challenge as such.  
Me: Okay.  
Them: The challenge is more, like, how do we get the most realistic concept the that that  
Me: Yes.  
Them: like, to get, like, actual data sources for real human pumps. So that's a bit different I guess, what we are talking about here. And when it comes to instructions and so on for like, our internal stack. We actually work with a lot of like, we we work with fine tuned models that that are kind of specifically fine tuned with certain system and  
Me: Okay.  
Them: and certain input, like, for example, we have we have a small 8,000,000,000 per meter model that we use for to feed with, like, whole websites. And generate, schema.org schema. That's, like, a very typical workflow. And basically, that's that model input is is very specific. It has to be in a certain way that it was, like, fine tuned with. And  
Me: Okay.  
Them: so there, I would say, like, the instruction optimization would be more on the actual fine tuning task as as  
Me: Okay.  
Them: as far as I would see it or even in a training from scratch where we would actually try to because we have a lot of repetitive workflows there. We would actually try to reduce the instructions or not even not need any instruction at all, but just like a token placeholder that basically  
Me: Okay.  
Them: represents the specific task that is needed.  
Me: Okay. Okay. I understand. That's more from from also from money perspective. Right? You're saving them. The token.  
Them: Exactly.  
Me: Okay. And then let me ask a BC,  
Them: And And  
Me: said do a lot of this manually. Right? So how much like, how do you identify if it's under or is it actually doing it? Do you look at, like, matrices or, like, test you have, like, your test dataset which you also use for training and then you invoke it with it or how do you do this? And how much time do you kind of spend on on, like, this manual back and forth and this manual adjustment?  
Them: Yeah. So, basically, I would say I have a I mean, from because I may maybe I'm a bit, like, victim of, like, doing that for a while already.  
Me: Yes.  
Them: Like, doing that for ten years now. So I have, like, a lot of, like, little you know, tools for myself where I have my, like, evaluation  
Me: Okay.  
Them: framework. And from from my experience, like, the most of the work is actually kind of trying to plug in your your custom data. For example, JSON schemas or you you know, whatever the output is, into your evaluation, like, matrix.  
Me: Okay.  
Them: That's where the where the work is, and  
Me: It's a checklist. Right? Like, or no checklist more as, like,  
Them: yeah. Whatever. Like, we it's like even there, it's like I found it tricky to have, like, a one size fits  
Me: Okay.  
Them: all solution because, like, the the data you're evaluating is always a bit  
Me: Mhmm.  
Them: different. And, also, at least from the tasks that that I'm working with most Also, the evaluation metrics you want, the KPIs are also usually a bit different, tailored to the task. So like, I found that using using, like, a standardized tool for that actually doesn't really  
Me: Okay.  
Them: do a lot of the heavy lifting, can't  
Me: It's  
Them: at from my experience.  
Me: we we had to build our own eval framework too and everything.  
Them: Mhmm.  
Me: It was very premature when we started two two, three years ago. So we kind of had to do Yeah. So yeah. And Gmail and all  
Them: But I also know  
Me: available deep eval is not enough. Like, everything we found kind of is yeah.  
Them: Mhmm.  
Me: We went through the same kind of journey. So you might have done it for ten years with all your little toolings, and you build your own evals, but yeah, we found that, for example, LLM as a judge is very  
Them: Mhmm.  
Me: yeah, it hallucinates too much as well. So you kind of we kind of went to more like a checklist based thingy. So you have your your credit criterias, and they can be yes, no. But you but then you get, like, a final score kind of. It's a classification rather than  
Them: Mhmm.  
Me: yeah, sentiment analysis because that's too too fickle.  
Them: Mhmm.  
Me: Yeah.  
Them: Right. Yeah. I mean but I also know that there are like, a lot of new tools out there and, like, I I do, like, every couple of months, I, like, try to set aside, like, a week to really, like, reset the the tooling.  
Me: Mhmm.  
Them: And I'm always really surprised with, like, how how much has changed. But then, like, after, like, like, a short honeymoon phase, like, not not with everything, but with, like, most of the tools, I'm kind of, like, like, a bit unimpressed. Like, in the end, it's like maybe it's a bit aligned with, like, how you see it with the no code  
Me: Yes, unlimited eventually. You start and after  
Them: There are just yeah.  
Me: two weeks, need something and you're too limited.  
Them: Yeah. Often, there is a reason for having code. Made in the first place. So because it just has a lot of flexibility to  
Me: Yep.  
Them: express something. And I think the challenge is with this fast moving in this fast moving world to identify what are the things that won't change or will likely  
Me: Okay.  
Them: stay the same? And then also trying to do a lot, like, on top of it, but kind of trying to solve those  
Me: Okay.  
Them: pain points. Yeah.  
Me: Okay. That's that's that's good. That's a good point, actually, also wanna make our sting an SDK more like a code plug and play, obviously, because it's for developers.  
Them: Mhmm.  
Me: But, you know, when we we're talking about optimization and changes, you know, we wanna showcase we wanna see somehow have a UI where you see the diffs. You know?  
Them: Mhmm.  
Me: Like the percent changes before and after so you can also when you plug it in online, like, we want to make it that it also works in production data, you can see also, like, your scores and all of this live. So there must be some there will be some kind of data UI where you look at data, you know, because looking at tables and data is always easier in a UI than just on, like, a log.  
Them: Mhmm.  
Me: So it's gonna be a mix, like, I guess, for us. But I completely agree with what you say that with the you have to figure out what's  
Them: Mhmm.  
Me: the static thing and what's the, what changes very fast. Yes.  
Them: Mhmm.  
Me: And we're also looking at hotel, like, the protocol because that's kind of seems to be now everybody or most of the solutions go on this OTEL protocol and have, like, some kind of a connector to it.  
Them: Yeah. Exactly. Like, I mean, I actually went recently through I I think I forgot most of the names, but through the options for observability tools for from LLM tasks specifically, but then circled back  
Me: Yep.  
Them: to, like, kind of the classic stack with Grafana and  
Me: Okay.  
Them: hotel and, like, Loki and so on because it just enables to to, like, funnel everything together into  
Me: Yes.  
Them: like, one process.  
Me: Okay.  
Them: And, and it is often, it is quite inter like, connect right, that you want to, like, that you want to monitor your, like, kind of like, model performance and and server and and and errors and so on at this  
Me: Okay.  
Them: same time. At least  
Me: Yeah. Makes sense. I think we use Mixpanel for this  
Them: my personal preference. Mhmm.  
Me: But yeah. I have now it's more like a a not so technical parts. Like, have two, three minutes on this. So it's about, like, releasing to production for you now with all of these various  
Them: Mhmm.  
Me: changing prompt instructions, you have customers  
Them: Mhmm.  
Me: at least I know kind of 20. Right? And we don't need the own detail. But if you now make changes on prompt, system instructions, maybe change the model in the back end, How what's your how do you feel about that? What's your, like, your personal experience, like, more from, like, a personal level, not from a technical, like like, you see do we have anxiety? Like, how do you make sure you're confident about the release? Yeah.  
Them: Right. Yeah. I mean, that I would say it's definitely tricky part. We we are also very new of the with the product. So we usually and we usually don't give us ourselves a lot of time to to have, like, staging environment where we really, like, thoroughly test everything.  
Me: Mhmm.  
Them: It's also I would say, like, one challenge that I definitely see is like, replicating the data for, like, realistic kind of staging environments and so on.  
Me: Mhmm.  
Them: Because you just have so much kind of variable, like, data and motion.  
Me: Yes.  
Them: That it's much more difficult to set up a realistic test environment, like when you just have a classical kind of application with with those parts. So  
Me: Okay. Deriving from your live data and from your live queries from customers actually getting, like, a test data set from this dot would help you prerelease test your functionality, and your degradation would be  
Them: Yes.  
Me: something which solves that, right?  
Them: Yeah. So I have to say, like, because we are a small team and because the customers are quite close to us, like, we should we should probably have like, much more, like, mature staging process, but we currently actually have services that are only production.  
Me: Okay.  
Them: That we we don't even have any test or staging environment for. And I see I see that with the machine learning setup, even more tricky because it's, it's usually, quite a significant chunk of tech and it's expensive. So  
Me: Yes.  
Them: it's it is expensive to replicate. We I think we are moving into a direction where this is a bit easier. We but there, again, we needed to build our own, like,  
Me: Okay.  
Them: custom flows. For dealing with the infrastructure components in a more flexible way.  
Me: Okay. Okay. And the but that that that's fine. And then for let let let us focus again on the the the  
Them: Mhmm.  
Me: prompt and the agent side of you. So what's your biggest pain from this 3C Like, pushing to production with confidence, getting the agent's life faster, or is it like maintaining the ones you have live? What's the biggest pain point of this tree?  
Them: I would say it's It is I think I would say, like, still is is moving faster and to have a, like, fluid  
Me: Continuous improvement  
Them: Yeah. Exactly. Exactly.  
Me: improvement Okay. Okay. That'd be an what features would help you do this? What is missing in your current flow stack? Or a stack that would allow you to do this faster? Is it data? Is it the the infrastructure? Is it evaluation  
Them: I I would say it's two things. It's it's first, kind of, like, good scaling mechanisms  
Me: Okay.  
Them: that are kind of tuned to your infrastructure.  
Me: Okay.  
Them: And the other thing is, kind of, yeah, data kind of data replication mechanism. So one of the most interesting tools I found recently on that front is actually not  
Me: Okay.  
Them: AI related at all. But helps a lot of that is called PG role.  
Me: Okay.  
Them: It's a postgres extension, that helps you maintaining to maintain different database schemas simultaneously.  
Me: Okay.  
Them: On the same database. And what that allows is that you can actually run different environments with different kind of data requirements on the same data.  
Me: Okay.  
Them: If that makes sense. And I think something similar if we had something similar for like, the overall stack, I'm actually surprised that that's so difficult to do these days that, because that's something I think would actually never change is that you can that you can almost, like, copy have, like, a safe copy of your or, like, a web  
Me: Yeah.  
Them: replica view instead of replicating the whole thing. You basically have a different view on your existing tech stack.  
Me: Okay.  
Them: That maybe has a bit less  
Me: Okay.  
Them: potential to change things. To to to to kind of, mess things up.  
Me: Okay.  
Them: So you can actually you can actually solve this problem by yeah, by having, like, different kind of staging test production views, without needing to, like, replicate  
Me: Think you answered all my questions. Now we can go. Like, now I would like to ask you also, like, if you have question about our solution, the one you're gonna do, and we're gonna explain a bit more in detail now. Maybe 12 to, like so if you wanna, like, optimize prompts or agent instructions, tool calling, so you need two things. You actually need to monitor and you need to create generate these AI insights kind of you're gonna need to see. You need to find the root cause. So you need to do kind of a root cause analysis. And the second thing is then you need to find countermeasures, like kind of an optimization algorithm that then optimizes against these, like, found root causes. So it's a two step process. Right? You like, that will manually, you would do the same if you have a lot of traces of your AI agent or your LLM calls and you would look through them, you'd be like you would score them, label them,  
Them: Mhmm.  
Me: either actually doing it or actually just like subconscious subconsciously do it and then figure out, okay, this is my root cause. Now I'm gonna fix it by adding this to the prompt. And then you usually what you do is you test it. Right? You would rerun the whole whole dataset way which you use for for which you analyzed and see, like, hey. Is this root cause still there, or is it fixed with your  
Them: Mhmm.  
Me: change? And we wanna solve this by actually like obviously, there's gonna be a trace connector, some kind of somehow you need to collect these traces. Then there's gonna be this a root con as cause analysis evaluation core, which does all of this which should generate these insights. And then obviously, this optimization engine, which  
Them: Mhmm.  
Me: then helps you or makes proposals, and it will show you basically the diff to the prior prompts or the diff to the prior  
Them: Mhmm.  
Me: instructions and the updated root cause analysis scoring. Right? Because you rerun, basically, You make the changes. And with the changes, you rerun, and then you see these scores changing.  
Them: Mhmm.  
Me: And then, obviously, you you ask to iteratively go to optimize your scores. Three times, five times, whatsoever, and, hopefully, you achieve a better goal.  
Them: Right.  
Me: Without degradation because this is kind of also why you need good events. So you don't  
Them: Mhmm.  
Me: obviously, you could remove the whole prompt and only say, look at this.  
Them: Mhmm.  
Me: And then, obviously, this root cause would be fixed, but then yeah, your system doesn't work anymore. So it needs to be, like,  
Them: Mhmm.  
Me: attuned. I mean, know it from AI. It's tuning, basically.  
Them: Mhmm.  
Me: It's the same process of, like, yeah, back propagation kind of, but on a prompt level. And  
Them: Right.  
Me: this is what we wanna look at. But, yes, we wanna show it to clients in a way that you see the diffs. Of, like, the actual code snippet you chain would change.  
Them: Mhmm.  
Me: So you can you you would have, like, a constructor which also gives us the prompt and everything, and then you could kind of manipulate this prompt, mutate it,  
Them: Why? Right. Right. Yeah. Mhmm. Right. Mhmm. Right. I I mean, my my prediction would be I know you have a hot stop now, actually, but, like, I would say my my prediction would be where the market might be going. I think we I would say there is a chance that we will see like, circling back from trying to do everything in text. To trying to go away from text in a way or, like, kind of have a merge. For example, one tool that I really like is Bumbled. To to deal with kind of JSON instructions or, like, kind of end end JSON input output, and I could imagine that there will be like, the successful players will probably deploy models that are more structured in terms of is it's already happening in the output, but also structured in inputs side. And so because it's a bit of a crutch right, to kind of experiment with different problems for the input, If you actually could have a, like, model that is as flexible but is clearer on the inputs as such, then it would give you an edge. I think it would solve a lot of problems. With the overall workflow to have almost again, like, pipe dream of, like, modeling of model model input where you can basically yeah, translate, like, a requirement into like, a a different kind of instruction that is more, is more structured and can I think that the missing pieces, like, to have a good actually, like, a a a good encoder, that that, like, a JSON and co or whatever encoder that has, like, a semi structured input into, like, a like, a functional instructions where you know they're gonna work? Basically. Mhmm. Sure. Yeah. Sounds good. It's good. Mhmm. Yeah. Yeah. Let's do it. Definitely. I I'm I'm curious where that goes. Yes. Okay. Thank good. Okay. Alles klar. Bis dann. Viel Erfolg. 