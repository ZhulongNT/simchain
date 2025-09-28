# Copilot Instructions for Simchain

## 项目架构概览
- Simchain 是一个用于教学和研究的区块链模拟器，核心目录为 `simchain/`。
- 主要模块：
  - `network.py`：区块链网络与节点管理，入口类为 `Network`。
  - `peer.py`：节点（Peer）实现，包含钱包、交易、区块链等。
  - `wallet.py`、`ecc.py`：钱包与密钥管理，支持 ECDSA。
  - `merkletree.py`：Merkle 树结构与验证。
  - `datatype.py`：核心数据类型（UTXO、Tx、Block 等）。
  - `lbc/`：格密码相关实验性模块。
  - 其他如 `base58.py`、`mnemonics.py` 为编码和助记词工具。

## 关键开发流程
- 构建/安装：
  - 推荐 `pip install simchain` 或 `python setup.py install`。
- 交互式用法：
  - 通过 `Network` 类创建区块链网络，模拟节点、交易、共识。
  - 示例：
    ```python
    from simchain import Network
    net = Network()
    net.peers[0].create_transaction(net.peers[1].addr, 100)
    net.consensus()
    ```
- 钱包与密钥：
  - 每个 Peer 拥有 Wallet，密钥对为 `SigningKey`/`VerifyingKey`，地址为 base58 编码。
  - 钱包可动态生成密钥对，支持多地址。

## 项目约定与模式
- 数据流：所有交易、区块、UTXO 都通过 Peer 对象流转，区块链状态由 Network 管理。
- 交易费用与奖励：每次交易会收取手续费，挖矿奖励由共识模块分配。
- 新节点加入时自动同步区块链。
- 代码风格：
  - 数据类型与结构体定义集中在 `datatype.py`。
  - 算法实现（如哈希、签名）分散在各自模块。
  - 注释率较低，建议 AI 生成代码时补充 docstring。

## 测试与调试
- 主要通过交互式 Python shell 进行功能验证。
- 没有标准化测试脚本，建议以 `README.md` 示例为基础编写测试。

## 依赖与集成
- 仅依赖 Python 标准库，无第三方区块链库。
- 格密码相关实验性代码在 `lbc/`，与主链逻辑隔离。

## 重要文件索引
- `simchain/network.py`：主入口，区块链网络与共识
- `simchain/peer.py`：节点与钱包
- `simchain/datatype.py`：核心数据结构
- `simchain/wallet.py`、`simchain/ecc.py`：密钥与签名
- `simchain/merkletree.py`：Merkle 树
- `simchain/lbc/`：格密码实验

---
如需补充说明或发现不清晰之处，请反馈具体模块或场景。
