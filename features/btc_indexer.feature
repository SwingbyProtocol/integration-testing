@btc_indexer @sub_minute

Feature: Test BTC indexer functionality

  # @cleanup.after_testrun
  # Scenario: Should clean up indexer clients
  #   Then all BTC indexer clients are stopped
  Background:
    When I start a new BTC indexer instance

  Scenario: Should connect and return a welcome connection
    Then I will receive a response containing the regex "Websocket connection is succesful" from the indexer

  @indexer_height
  Scenario: Should be within 2 block of BlockCypher height
    When I get the current BTC height from "BlockCypher"
    Then the indexer height should be within 2 block of it

  # @test
  # Scenario: Should receive the latest transaction from the indexer
  #   And I get the latest BTC transaction from "BlockCypher"
  #   Then the indexer should recognise the latest BTC transaction

  # Scenario: Should return a set of transactions
  #   When I start a new BTC indexer instance
  #   When a "getTx" action is sent to the BTC indexer for address "1KFHE7w8BhaENAswwryaoccDb6qcT6DbYY"  

  # Scenario: should get the latest mempool
  # scenario: should watch address and receive latest transactions

  @cleanup.after_testrun
  Scenario: Clean up all node indexer connections
    # no clients to clena up (all http)
    Then all indexer clients are disposed
