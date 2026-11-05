# app-name-check

An agent skill that names your iOS app so people can find it. Built for Claude Code, Cursor, Codex and anything else that reads skills.

Most apps launch to zero downloads because they're named after an idea, and people search for what an app does. This skill reads your project, finds searches that fit, checks them against live App Store results and writes your listing.

```
npx skills add dyuven123/app-name-check
```

Then ask your agent: *"What should I call this app in the US and Germany?"*

## What's inside

**The rules**, measured on 350,712 App Store searches in 87 countries and 82,926 new apps:

| Name of a new app in the top 25, under 100 ratings | Top 3 | Top 10 |
|---|---|---|
| Exactly the search | 15.2% | 43% |
| Starts with the search, then more words | 9.1% | 36% |
| "Brand: search", after a separator | 3.5% | 32% |
| Search not in the name | 2.9% | 27% |

[Full research](https://lazyaso.com/research/new-app-names)

**A free name check.** No key, no signup, no dependencies:

```
python3 skills/app-name-check/scripts/name_check.py "sky map" --country us
```

```json
{ "starts_with_it": 4, "mid_name": 5, "call": "taken" }
```

## Want the search demand too?

The public API shows whether a name is free, not how many people search it. [Lazy ASO](https://lazyaso.com/?ref=github) is my Mac app that gives your AI Apple's official search lists in 87 countries, every free name with a measured chance, daily rank checks and upload to App Store Connect. Coming soon.

## License

MIT
