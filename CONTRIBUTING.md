# 贡献指南 | Contributing Guide

感谢你考虑为WangChain做出贡献！
Thank you for considering contributing to WangChain!

## 如何贡献 | How to Contribute

### 报告问题 | Reporting Issues

如果你发现了bug或有功能建议：
If you find a bug or have a feature suggestion:

1. 检查 [Issues](https://github.com/Puppy4388/WangChain/issues) 确保问题未被报告
2. 创建新的Issue，提供详细信息：
   - 问题描述 Problem description
   - 重现步骤 Steps to reproduce
   - 预期行为 Expected behavior
   - 实际行为 Actual behavior
   - 环境信息 Environment info (Python version, OS, etc.)

### 提交代码 | Submitting Code

1. **Fork仓库 Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/WangChain.git
   cd WangChain
   ```

2. **创建分支 Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **安装开发依赖 Install development dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

4. **进行修改 Make your changes**
   - 遵循现有代码风格 Follow existing code style
   - 添加必要的测试 Add necessary tests
   - 更新文档 Update documentation
   - 确保代码有中英双语注释 Ensure code has bilingual comments

5. **运行测试 Run tests**
   ```bash
   pytest tests/ -v
   ```

6. **代码格式化 Format code**
   ```bash
   black wangchain/ tests/ examples/
   flake8 wangchain/ tests/ examples/
   ```

7. **提交更改 Commit changes**
   ```bash
   git add .
   git commit -m "feat: add new feature" # or "fix: fix bug"
   ```

   提交信息格式 Commit message format:
   - `feat:` 新功能 New feature
   - `fix:` Bug修复 Bug fix
   - `docs:` 文档更新 Documentation update
   - `test:` 测试相关 Test related
   - `refactor:` 重构 Refactoring
   - `style:` 代码格式 Code formatting

8. **推送并创建PR Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   然后在GitHub上创建Pull Request

## 代码规范 | Code Standards

### Python代码风格 | Python Code Style

- 遵循 PEP 8 Follow PEP 8
- 使用类型提示 Use type hints
- 最大行长度120字符 Max line length: 120 characters
- 使用Black格式化代码 Use Black for formatting

### 文档注释 | Documentation

所有公共函数、类和模块必须有文档字符串：
All public functions, classes, and modules must have docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """
    函数简介 - Function brief
    
    详细描述（中文）
    Detailed description (English)
    
    Args:
        param1: 参数1描述 Parameter 1 description
        param2: 参数2描述 Parameter 2 description
        
    Returns:
        返回值描述 Return value description
        
    Raises:
        异常描述 Exception description
    """
    pass
```

### 测试要求 | Testing Requirements

- 所有新功能必须有测试 All new features must have tests
- 保持测试覆盖率 >80% Maintain test coverage >80%
- 测试应该清晰易懂 Tests should be clear and understandable
- 使用有意义的测试名称 Use meaningful test names

```python
def test_feature_name_expected_behavior():
    """测试描述 - Test description"""
    # Arrange
    # Act
    # Assert
    pass
```

## 开发工作流 | Development Workflow

### 本地开发 | Local Development

1. **设置环境变量 Set up environment**
   ```bash
   cp .env.example .env
   # 编辑.env文件添加API密钥
   # Edit .env file to add API keys
   ```

2. **运行示例 Run examples**
   ```bash
   python examples/basic_llm_example.py
   python examples/rag_example.py
   python examples/agent_example.py
   ```

3. **运行测试 Run tests**
   ```bash
   # 运行所有测试 Run all tests
   pytest
   
   # 运行特定测试 Run specific tests
   pytest tests/test_config.py
   
   # 显示覆盖率 Show coverage
   pytest --cov=wangchain --cov-report=html
   ```

### 添加新功能 | Adding New Features

1. **规划设计 Plan and design**
   - 考虑设计模式 Consider design patterns
   - 确保可扩展性 Ensure extensibility
   - 考虑向后兼容 Consider backward compatibility

2. **实现功能 Implement feature**
   - 遵循现有架构 Follow existing architecture
   - 使用适当的设计模式 Use appropriate design patterns
   - 添加中英双语注释 Add bilingual comments

3. **编写测试 Write tests**
   - 单元测试 Unit tests
   - 集成测试（如需要）Integration tests (if needed)
   - 边界情况测试 Edge case tests

4. **更新文档 Update documentation**
   - 更新README.md Update README.md
   - 更新ARCHITECTURE.md（如需要）Update ARCHITECTURE.md (if needed)
   - 添加示例代码 Add example code

## 设计原则 | Design Principles

### SOLID原则 | SOLID Principles

- **S - 单一职责 Single Responsibility**: 每个类只有一个职责
- **O - 开闭原则 Open/Closed**: 对扩展开放，对修改关闭
- **L - 里氏替换 Liskov Substitution**: 子类可以替换父类
- **I - 接口隔离 Interface Segregation**: 使用专门的接口
- **D - 依赖倒置 Dependency Inversion**: 依赖抽象而非具体

### 设计模式 | Design Patterns

优先使用以下设计模式：
Prefer the following design patterns:

- 工厂模式 Factory Pattern
- 构建器模式 Builder Pattern
- 单例模式 Singleton Pattern
- 策略模式 Strategy Pattern（可扩展）
- 装饰器模式 Decorator Pattern（可扩展）

## 代码审查 | Code Review

提交的PR将会被审查：
Submitted PRs will be reviewed for:

- ✅ 代码质量 Code quality
- ✅ 测试覆盖 Test coverage
- ✅ 文档完整性 Documentation completeness
- ✅ 设计合理性 Design rationality
- ✅ 性能考虑 Performance considerations
- ✅ 安全性 Security

## 社区行为准则 | Code of Conduct

### 我们的承诺 | Our Pledge

- 尊重所有贡献者 Respect all contributors
- 包容不同观点 Be inclusive of different viewpoints
- 接受建设性批评 Accept constructive criticism
- 关注对社区最有利的事 Focus on what's best for the community

### 不可接受的行为 | Unacceptable Behavior

- 人身攻击 Personal attacks
- 骚扰行为 Harassment
- 发布他人隐私 Publishing others' private information
- 其他不专业行为 Other unprofessional conduct

## 获得帮助 | Getting Help

如需帮助，可以：
For help, you can:

- 查看文档 Check documentation
- 搜索已有Issues Search existing issues
- 在Discussions中提问 Ask in Discussions
- 创建新Issue Create a new issue

## 许可证 | License

贡献的代码将采用MIT许可证
Contributed code will be licensed under the MIT License

---

再次感谢你的贡献！🎉
Thank you again for your contribution! 🎉
