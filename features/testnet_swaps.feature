@testnet @swaps @sub_hour

Feature: Test node swaps functionality

  Background: Stop nodes before test
    # check our environment has enough balance for tests
    # Given each of my wallets has more than 3.1 coins

  @send_BTC.B
  Scenario: send BTC.B tokens
    When I send 5.0 "BTCB-1DE" to the address "tbnb1hzmm62lape793rju0dek5ecr83qlh6q608uuzn"

  Scenario: adds more float to BTC side
    When I send 10.42 "BTC" to the address "mr6ioeUxNMoavbr2VjaSbPAovzzgDT7Su9"

  @add_float_BTC
  Scenario: adds more float to BTC side
    When I send 10.42 "BTC" to the address "mr6ioeUxNMoavbr2VjaSbPAovzzgDT7Su9"

  @add_flaot_BTC.B
  Scenario: adds more float to BTC.B side
    When I send 10.42 "BTCB-1DE" to the address "tbnb1ws2z8n9ygrnaeqwng69cxfpnundneyjze9cjsy"

  @testnet @spend @sBTC
  Scenario: Performing a swap from BTC to BTCB-1DE funds my wallet correctly
    Given I check my "BTCB-1DE" balance
    When I perform a swap from "BTC" to "BTCB-1DE" for 10.105 on testnet
    # test swap now exists in the KV store
    # test swap has WAITING status
    # test original transac
    And I wait for my "BTCB-1DE" balance to change
    Then my "BTCB-1DE" balance has increased by at least 0.105

  @testnet @spend @BTC.B
  Scenario: Performing a swap from BTCB-1DE to BTC funds my wallet correctly
    Given I check my "BTC" balance
    When I perform a swap from "BTCB-1DE" to "BTC" for 3.005 on testnet
    And I wait for my "BTC" balance to change
    Then my "BTC" balance has increased by at least 3.0

  @testnet @refund @BTC
  Scenario: Performing a swap from BTCB-1DE to BTC but with an invalid address will refund me
    When I send 0.0015 "BTCB-1DE" to the address "tbnb1ws2z8n9ygrnaeqwng69cxfpnundneyjze9cjsy"
    And I wait for 5 seconds
    # reset balance check
    And I check my "BTCB-1DE" balance
    # wait for refund to send
    And I wait for my "BTCB-1DE" balance to change
    Then my "BTCB-1DE" balance has increased by at least 0.001

  @testnet @refund
  Scenario: Performing a swap from BTC to BTCB-1DE but with an invalid address will refund me
    When I check my "BTC" balance
    When I send 0.0015 "BTC" to the address "mr6ioeUxNMoavbr2VjaSbPAovzzgDT7Su9"
     # wait for first send to confirm
    And I wait for my "BTC" balance to change
    # reset balance check
    And I check my "BTC" balance
    # wait for refund to send
    And I wait for my "BTC" balance to change
    Then my "BTC" balance has increased by at least 0.0008
  
  @volume
  Scenario: Performing a swap from BTC to BTCB-1DE funds my wallet correctly
    Given my "BTC" balance is more than 0.5
    When I perform a swap from "BTC" to "BTCB-1DE" for a random small amount on testnet

  @volume
  Scenario: Performing a swap from BTCB-1DE to BTC funds my wallet correctly
    Given my "BTCB-1DE" balance is more than 0.5
    When I perform a swap from "BTCB-1DE" to "BTC" for a random small amount on testnet

  #Scenario: Sending a BTC float to the network will be accepted
  #Scenario: Sending a BTCB-1DE float to the network will be accepted
