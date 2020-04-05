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
      | Moniker          | Host            | ApiPort |
      | testnet_node_1   | 13.229.46.145   | 8067    |
      | testnet_node_2   | 13.229.46.145   | 8068    |
      | testnet_node_3   | 13.229.46.145   | 8069    |
      | testnet_node_4   | 54.255.211.108  | 8070    |
      | testnet_node_5   | 54.255.211.108  | 8071    |
      | testnet_node_6   | 54.255.211.108  | 8072    |
      | testnet_node_7   | 54.255.211.108  | 8073    |
      | testnet_node_8   | 54.255.210.204  | 8074    |
      | testnet_node_9   | 54.255.210.204  | 8075    |
      | testnet_node_10  | 54.255.210.204  | 8076    |
      | testnet_node_11  | 52.77.248.216   | 8077    |
      | testnet_node_12  | 52.77.248.216   | 8078    |
      | testnet_node_13  | 52.77.248.216   | 8079    |
      | testnet_node_14  | 54.254.185.97   | 8080    |
      | testnet_node_15  | 54.254.185.97   | 8081    |
      | testnet_node_16  | 54.254.185.97   | 8082    |
      | testnet_node_17  | 54.169.226.134  | 8083    |
      | testnet_node_18  | 54.169.226.134  | 8084    |
      | testnet_node_19  | 54.169.226.134  | 8085    |
      | testnet_node_20  | 54.254.220.51   | 8086    |
      | testnet_node_21  | 54.254.220.51   | 8087    |
      | testnet_node_22  | 54.254.220.51   | 8088    |
      | testnet_node_23  | 52.77.234.40    | 8089    |
      | testnet_node_24  | 52.77.234.40    | 8090    |
      | testnet_node_25  | 52.77.234.40    | 8091    |
    Then all the Swingby nodes return a valid status with the version "0.1.0"

  @cleanup.after_testrun
  Scenario: Clean up all node clients
    # no clients to clena up (all http)
