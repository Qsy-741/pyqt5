from PyQt5.QtGui import QFont, QColor, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtCore import QRegExp


# 语法高亮类
class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        self.highlightingRules = []

        # 关键字规则
        keywords = [
            "and", "as", "assert", "break", "class", "continue", "def",
            "del", "elif", "else", "except", "False", "finally", "for",
            "from", "global", "if", "import", "in", "is", "lambda",
            "None", "nonlocal", "not", "or", "pass", "raise", "return",
            "True", "try", "while", "with", "yield"
        ]
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor(0, 0, 255))
        keywordFormat.setFontWeight(QFont.Bold)
        for keyword in keywords:
            pattern = f"\\b{keyword}\\b"
            rule = HighlightingRule(pattern, keywordFormat)
            self.highlightingRules.append(rule)

        # 字符串规则
        stringFormat = QTextCharFormat()
        stringFormat.setForeground(QColor(180, 0, 0))
        self.highlightingRules.append(HighlightingRule("\".*\"", stringFormat))
        self.highlightingRules.append(HighlightingRule("\'.*\'", stringFormat))

        # 注释规则
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(QColor(0, 128, 0))
        self.highlightingRules.append(HighlightingRule("#[^\n]*", commentFormat))

    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = QRegExp(rule.pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule.format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)


class HighlightingRule():
    def __init__(self, pattern, format):
        self.pattern = pattern
        self.format = format




