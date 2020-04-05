@local @swaps @sub_hour

Feature: Test node swaps functionality

#   # top up float
#   # When I send 0.42 "BTC" to the nodes TSS address
#   # When I send 0.42 "BTC.B-918" to the nodes TSS address with the memo "float"
#   # When I send 0.42 "BNB" to the nodes TSS address with the memo "float"

  # Background: Stop nodes before test
  #   # check our environment has enough balance for tests
  #   Given each of my wallets has more than 0.2 coins
  #   Given each of the node TSS wallets has more than 0.2 coins
    # Spin up 3 nodes using fully generated keystores

  @start_local
  Scenario:
    When I start a new local Swingby node instance with the flags "--p2p.port=12121 --rest.port=8067 --preset=101"
    When I start a new local Swingby node instance with the flags "--p2p.port=12122 --p2p.connect=127.0.0.1:12121 --rest.port=8068 --preset=102"
    When I start a new local Swingby node instance with the flags "--p2p.port=12123 --p2p.connect=127.0.0.1:12122 --rest.port=8069 --preset=103"
    Then I wait for 2 hours

#   Scenario: Performing a swap from BTC to BTC.B funds my wallet correctly
#     Given I check my "BTC.B-918" balance
#     When I perform a swap from "BTC" to "BTC.B-918" for 0.0042
#     And I wait for my "BTC.B-918" balance to change
#     Then my "BTC.B-918" balance has increased by at least 0.00418
