@peers @sub_minute

Feature: Test node peer functionality

  # @local
  # Scenario: Should begin listening for peer connections
  #   When I start a new local Swingby node instance with the flags "--p2p.port=12121 --rest.port=8067 --preset=1"
  #   Then the total network peer count is 1
  #   When I start a new local Swingby node instance with the flags "--p2p.port=12122 --p2p.connect=127.0.0.1:12121 --rest.port=8068 --preset=2"
  #   Then the total network peer count is 2

  @testnet
  Scenario: Testnet network should have atleast 15 nodes on the newtork
    # 15 nodes = minimum for TSS threshold
    Then the testnet network has more than 15 nodes

  @testnet
  Scenario: All peers on the tesnet network should be pingable
    Given I request the Swingby node status for the instances
      | Moniker         | Host                            | ApiPort |
      | testnet-node-1  | testnet-node.swingby.network    | 443     |
      | testnet-node-2  | testnet-node-2.swingby.network  | 443     |
      | testnet-node-3  | testnet-node-3.swingby.network  | 443     |
      | testnet-node-4  | testnet-node-4.swingby.network  | 443     |
      | testnet-node-5  | testnet-node-5.swingby.network  | 443     |
      | testnet-node-6  | testnet-node-6.swingby.network  | 443     |
      | testnet-node-7  | testnet-node-7.swingby.network  | 443     |
      | testnet-node-8  | testnet-node-8.swingby.network  | 443     |
      | testnet-node-9  | testnet-node-9.swingby.network  | 443     |
      | testnet-node-10 | testnet-node-10.swingby.network | 443     |
      | testnet-node-11 | testnet-node-11.swingby.network | 443     |
      | testnet-node-12 | testnet-node-12.swingby.network | 443     |
      | testnet-node-13 | testnet-node-13.swingby.network | 443     |
      | testnet-node-14 | testnet-node-14.swingby.network | 443     |
      | testnet-node-15 | testnet-node-15.swingby.network | 443     |
      | testnet-node-16 | testnet-node-16.swingby.network | 443     |
      | testnet-node-17 | testnet-node-17.swingby.network | 443     |
      | testnet-node-18 | testnet-node-18.swingby.network | 443     |
      | testnet-node-19 | testnet-node-19.swingby.network | 443     |
      | testnet-node-20 | testnet-node-20.swingby.network | 443     |
      | testnet-node-21 | testnet-node-21.swingby.network | 443     |
      | testnet-node-22 | testnet-node-22.swingby.network | 443     |
      | testnet-node-23 | testnet-node-23.swingby.network | 443     |
      | testnet-node-24 | testnet-node-24.swingby.network | 443     |
      | testnet-node-25 | testnet-node-25.swingby.network | 443     |
    Then all the Swingby nodes return a valid status with the version "0.1.0"

  @cleanup.after_testrun
  Scenario: Clean up all node clients
    # no clients to clena up (all http)
