# aiogramTemplate
Simple telegram-bot template with aiogram pylib

### Background info


`The difference between aiogram 3.x and 2.x:` 

- The second version handled `only text messages` by default, while the third version handles `any type of message` by default.

- There are two types of middlewares: `Outer` and `Inner`. Outer are executed **before** the filters start checking, and inner are executed **after**.
- `Inner-middleware` on Update is always called (i.e. there is no difference between `Outer` and `Inner` in this case).
- Middlewares on Update `can only be hung on the dispatcher` (root router).