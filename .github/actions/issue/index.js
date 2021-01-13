const github = require('@actions/github');
const core = require('@actions/core');

async function run() {
  try{
    // This should be a token with access to your repository scoped in as a secret.
    // The YML workflow will need to set myToken with the GitHub Secret Token
    // myToken: ${{ secrets.GITHUB_TOKEN }}
    // https://help.github.com/en/actions/automating-your-workflow-with-github-actions/authenticating-with-the-github_token#about-the-github_token-secret
    const token = core.getInput('token');
    const title = core.getInput('title');
    const body = core.getInput('body');
    const assignees = core.getInput('assignees');

    const octokit = github.getOctokit(token)

    const response = await octokit.issues.create({
      owner: github.context.repo.owner,
      repo: github.context.repo.repo,
      //...github.context.repo,
      title,
      body,
      assignees: assignees ? assignees.split('\n') : undefined
    });

    core.setOutput('issue', JSON.stringify(response.data));
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();