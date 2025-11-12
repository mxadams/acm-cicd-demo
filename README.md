# ACM CI/CD Workshop Activity

This repo has a very basic REST API written in Python which returns JSON
indicating whether a number is even.

There are two parts to this activity. I strongly recommend you do them in
order.

## Part 1: Run unit tests with pytest

Start by **forking** this repo so that you can make changes to it.

The rest of the project involves changing some of the files in the repo. You
can either clone it to your IDE, or you may find the steps simple enough that
the GitHub built-in web editor is enough.

Start by looking at `.github/workflows/cicd.yml`. This function declares an
Action that GitHub will run. It is written in a language called YAML. In this
case the top few lines tell GitHub to run the action whenever a commit is
pushed to the `main` branch.

I've ~~vibe~~ coded a few unit tests to make sure the underlying logic of my
`isEven` function is correct. Let's run these every time we push to GitHub.

Change the first TODO to
```
      - uses: actions/checkout@v4
```
Anyone can publish an action to GitHub—including GitHub itself, which is the
publisher of this "check out" action. This clones the repo to the container in
which the action runs.

To set up the Python environment (2nd TODO), add the following:
```
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - name: Install uv
        run: pip install uv
      - name: Install dependencies
        run: uv sync
```
Here we see a bit of extra syntax, where `setup-python` takes an option. More
sophisticated actions have lots of options. The GitHub docs have an extensive
reference of all the things one can do.

`run` is the syntax to run a shell command. You could run `ls` or `cat foo`
here if you wanted. In this case, we're using `uv`. If you're not familiar with
it, it's a tool that handles managing your Python project and its dependencies.

For the third TODO, we run the tests, which is the command `uv run pytest`:
```
      - name: Run tests
        run: uv run pytest
```

Commit these changes and push to GitHub. You should see a green checkmark next
to your commit! If you click on it, you can see these commands being run.

## Part 2: Deploy the application with Fly.io

For this part, you'll need to make an account at https://fly.io

You'll then need to go into the dashboard and connect your GitHub fork to Fly.io.
> Note: You might be thinking, "Shouldn't we configure this part in Git, too?"
> You'd be right—we'd use an infrastructure as code tool like Terraform to do
> that. However, that's beyond the scope of this tutorial.

Try deploying stuff manually and making sure it works.

Next, generate an API key. You can do this in the web dashboard under the
"Tokens" option in the sidebar.

Add the API key to your secrets in GitHub by going to repo settings -> Actions
-> secrets and pasting the key into a secret named `FLY_API_TOKEN`.

Fly has an automagic tool that builds everything, and a GitHub action that
wraps all the setup. You can add it with
```
      - uses: actions/checkout@v4
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```
