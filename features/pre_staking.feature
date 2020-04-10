@testnet @staking

# Testnet api found at staking-api.swingby.network
Feature: Test pre-staking API functionality
    Scenario: Sending a self-stake transaction is recorded in the API
        Given my "SWINGBY-888" balance is more than 10.0
        When I request the current weeks pre-staking memo
        When I send 1.1 "SWINGBY-888" to the address "tbnb1dedxffvl324ggfdpxl0gw5hwylc848ztuy7g7c" with that memo
        # Test that the stake has been received

    Scenario: Reward hist endpoint is reachable
        When I request the current weeks pre-staking rewards for the address "tbnb1z20t7rn6urh46m2tavny3ap9n0pvkf47mynuza"
        # Exception raised if not 2xx status code

    Scenario: Weekly memo endpoint is reachable
        When I request the current weeks pre-staking memo
        # Exception raised if not 2xx status code

    Scenario: Payout endpoint is reachable
        When I request the current weeks pre-staking payout
        # Exception raised if not 2xx status code

    Scenario: Staking leaderboard endpoint is reachable
        When I request the current weeks pre-staking leaderboard
        # Exception raised if not 2xx status code

    Scenario: Floats endpoint is reachable
        When I request the network floats
        # Exception raised if not 2xx status code

    Scenario: Platform status endpoint is reachable
        When I request the network platform status
        # Exception raised if not 2xx status code

    Scenario: Swingby asset endpoint is reachable
        When I request the Swingby asset info
        # Exception raised if not 2xx status code

    Scenario: Stakes endpoint is reachable
        When I request the current weeks pre-staking stakes for the address "tbnb1z20t7rn6urh46m2tavny3ap9n0pvkf47mynuza"
        # Exception raised if not 2xx status code

    Scenario: Holders endpoint is reachable
        When I request the current weeks pre-staking holders
        # Exception raised if not 2xx status code
