## 阶段 6：LaTeX 排版与 PDF 编译（是否需要执行取决于用户前面的回答）

### 6.1 排版原则

采用极简风格：

- 无装饰：无彩色框、无线框、无背景色块
- 纯文字层次：仅通过标题、列表、表格、公式组织内容
- 高信息密度：每页包含尽可能多的关键信息
- 黑白打印友好：纯黑色文字，无灰度依赖

### 6.2 章节分类方式

章节分类不使用彩色框或塑料质感装饰，仅靠：

- § 符号 + 罗马数字（如 §I、§II）标识大章
- 阿拉伯数字（如 1.、2.）标识节
- 小写字母（如 (a)、(b)）标识小节

### 6.3 LaTeX 模板

使用以下最小模板（保存为 主文件.tex）：

```latex
\documentclass[12pt,a4paper]{article}
\usepackage[UTF8]{ctex}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{geometry}
\geometry{left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}
\usepackage{parskip}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.8ex plus 0.2ex minus 0.2ex}

% 定理环境（无框、无装饰）
\newtheorem{definition}{定义}[section]
\newtheorem{theorem}{定理}[section]
\newtheorem{example}{示范例题}[section]
\newtheorem{exercise}{引导练习}[section]
\newtheorem{problem}{独立习题}[section]

% 章节标题格式（朴素、无装饰）
\usepackage{titlesec}
\titleformat{\section}{\large\bfseries}{§\Roman{section}}{1em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\arabic{subsection}.}{1em}{}
\titleformat{\subsubsection}{\normalsize\itshape}{(\alph{subsubsection})}{1em}{}

%元数据（按讲义实际情况填写）
\title{讲义标题}
\author{作者}
\date{\today}

\begin{document}
\maketitle
\tableofcontents
\newpage

% 各章内容（通过 \input 引入）
\input{01-第一章标题}
\input{02-第二章标题}
% 在此继续添加更多章节

\end{document}
```

每章单独保存为 NN-<章标题>.tex，内容结构如下{节标题}

```latex

\section{章标题}

\subsection{节标题}

正文内容...

\subsection{节标题}

\begin{example}
示范例题内容
\end{example}

\begin{exercise}[提示]
引导练习内容
\end{exercise}

\begin{problem}
独立习题内容
\end{problem}

\subsection{本章小结}
回顾核心要点，预告下一章。
```

### 6.4 PDF 编译

仅在已选择 PDF 输出并通过必要审稿后编译；先确认编译器与中文字体可用。
编译命令（使用 latexmk）：

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error 主文件.tex 2>&1 | tee compile.log
```

若编译失败：

1. 读取 compile.log 定位错误
2. 修复 .tex 源文件中的 LaTeX 语法错误
3. 重新编译（最多重试 2 次）
   若 2 次重试后仍失败，停止编译并向用户报告具体错误位置。


## 编译验证

Markdown 单美元约定仅适用于 Markdown。LaTeX 展示公式使用 \[...\] 或 amsmath 环境。模板输入文件要改为真实章节。独立单文件文档在 Codex 内优先用内置编译器，多文件项目使用支持该结构的本地工具。

总计初次编译加最多两次修复重试；失败保留源文件并报告具体位置，工具缺失时不宣称成功。检查实际 PDF 的中文、公式、目录与分页，有渲染工具时逐页检查；无法视觉检查时明确说明。转换不改变数据、引文与论断；实质修改重新送审。
