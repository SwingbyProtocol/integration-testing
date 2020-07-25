@testnet @swaps @sub_hour

Feature: Test node swaps functionality

  Background: Stop nodes before test
    # check our environment has enough balance for tests
    # Given each of my wallets has more than 3.1 coins

  @add_float_BTC
  Scenario: adds more float to BTC side
    When I send 10.42 "BTC" to the address "mr6ioeUxNMoavbr2VjaSbPAovzzgDT7Su9"

  @add_flaot_BTC.B
  Scenario: adds more float to BTC.B side
    When I send 10.42 "BTC.B-888" to the address "tbnb1ws2z8n9ygrnaeqwng69cxfpnundneyjze9cjsy"

  @testnet @spend @sBTC
  Scenario: Performing a swap from BTC to BTC.B-888 funds my wallet correctly
    Given I check my "BTC.B-888" balance
    When I perform a swap from "BTC" to "BTC.B-888" for 0.105 on testnet
    And I wait for my "BTC.B-888" balance to change
    Then my "BTC.B-888" balance has increased by at least 0.105

  @testnet @spend @BTC.B
  Scenario: Performing a swap from BTC.B-888 to BTC funds my wallet correctly
    Given I check my "BTC" balance
    When I perform a swap from "BTC.B-888" to "BTC" for 3.005 on testnet
    And I wait for my "BTC" balance to change
    Then my "BTC" balance has increased by at least 3.0

  @testnet @refund @BTC
  Scenario: Performing a swap from BTC.B-888 to BTC but with an invalid address will refund me
    When I send 0.0015 "BTC.B-888" to the address "tbnb1ws2z8n9ygrnaeqwng69cxfpnundneyjze9cjsy"
    And I wait for 5 seconds
    # reset balance check
    And I check my "BTC.B-888" balance
    # wait for refund to send
    And I wait for my "BTC.B-888" balance to change
    Then my "BTC.B-888" balance has increased by at least 0.001

  @testnet @refund
  Scenario: Performing a swap from BTC to BTC.B-888 but with an invalid address will refund me
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
  Scenario: Performing a swap from BTC to BTC.B-888 funds my wallet correctly
    Given my "BTC" balance is more than 3.5
    When I perform a swap from "BTC" to "BTC.B-888" for a random small amount on testnet

  @volume
  Scenario: Performing a swap from BTC.B-888 to BTC funds my wallet correctly
    Given my "BTC.B-888" balance is more than 3.5
    When I perform a swap from "BTC.B-888" to "BTC" for a random small amount on testnet

  #Scenario: Sending a BTC float to the network will be accepted
  #Scenario: Sending a BTC.B-888 float to the network will be accepted
