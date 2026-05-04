# TempRepo: a template for repositories

Here, you should present the project in few setences.


## Install:

Install instruction, with dependancy description.

The `install` script in `bin` directory authomatize the install process.

```sh
./bin/install.sh
```

## Get Stated:

Get started instruction.


## Documentation

The documentation is on [Markdown](https://en.wikipedia.org/wiki/Markdown) format starting by `index.md` in the `docs` directory.
It can be served as a _HTML_ web site thanks to [MkDocs](https://www.mkdocs.org/).

```sh
mkdocs serve
```

You can then refer to the [http://127.0.0.1:8000/](documentation).
The navigation structure is defined on the `mkdocs.yml` file.


## Contributes

The project developments relies on several tools: 

### Git

- **Git** is a decentralized solution for version management. Its first feature is to allow several contributors to work on a same directory, each one on its own machine.
It permits to share an entire historic of all modifications through a common *repository* on a server, to facilitate fusion of document version (mainly by using text format), and to do it in a safe way.

- A **GitServer**, *Bitbucket*, *GitHub*, [framagit](https://framagit.org) or a private install of gitlab, propose solutions based on *git* to share a repository in the cloud with management services (groups, members, access rules).

- **Markdown Documents**: _Markdown_ is a text format, very simple and directly interpretable on all _git_ server solutions. The format follows the philosophy: **What you see is what you get**

- Going further with Git:
    * [Learn Git](https://try.github.io/)
    * [GitForWindows](https://gitforwindows.org/) a simple IDE for Windows.
    * [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### toml config file

Configuration file relies on a simple [toml text format](https://fr.wikipedia.org/wiki/TOML).
Python and shell tools can be installed with `pip`.

```sh
pip install toml toml-cli
```

Default config file is proposed in `bin/default-config.toml` and have been copied in root directory of the repository as `config.toml` at install step.

Usage exemple in terminal: 

```sh
toml get webpages.module
```

### Github pages 

Doc. deployment is achieved with a public github repository (_temprepo-site.github.io.git_), by copying the _mkdocs_ generated site in the `lct-pls` directory of this public repository.

```sh
mkdocs build
git clone git@github.com:temprepo-site/temprepo-site.github.io.git ../temprepo-site
rm -fr ../temprepo-site-site/lct-pls
mv ./site ../temprepo-site-site/lct-pls
git -C ../temprepo-site-site commit -am "lct-pls updates"
git -C ../temprepo-site-site push
```

For convenience, this manipulation is automatized with the script `./bin/docs-deploy.sh`.
To notice that the documentation repository can be cloned anywhere on your computer while your `config.toml` is updated accordingly.

### Slide Presentations

The presentation/slides are prepared using `marp` (an extantion to Markdown permiting to generate slides pdf).
`marp` is fully integrated to VisualCode:

- Get *Marp for VS Code* extention
- On `VS Code parameters > working space > Marp for VS Code` you can add elements on `Markdown › Marp: Themes` : `slides/slides.css`.
- Also authorise html tag. activate `all` in `marp: HTML` setting.

### Overleaf Web-Editor

[Overleaf](https://www.overleaf.com) is a Latex dedicated web-editor.

It is possible to clone locally overleaf project based on `git` tool.
It supposes that you create an identifiaction token on your _overleaf.com_ settings.
For instance to clone a `PROJECT-NAME` from the overleaf code `CODE` : 

```bash
git clone https://git@git.overleaf.com/$CODE $PROJECT-NAME
```

By convention, we recommand to build the project name as `PROJECT-NAME= ovl-$Author-$PROJECT-$YEAR`

CODE                     | Author   | PROJECT               | DATE      |
-------------------------|----------|-----------------------|-----------|
6661a9f3e44db0c19fde4c5b | Naury    | SAC                   | 2025      |
67c85987f374a5ffcce204ab | Ltaif    | DCIA                  | 2025      |
6797af19d58c0412ab4da125 | Gouget   | IROS                  | 2025      |
67ed28f0d11dfd6972fa3e09 | Alie     | PAIS                  | 2025      |

