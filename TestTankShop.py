import pytest
from TankShop import Shop
import mock


class TestTankShop():

    @pytest.fixture(scope="class")
    def resource_setup(self):
        player = mock.Mock()
        player.inventoryPlanes = []
        player.inventoryGuns = []
        player.saveResources.return_value = 'ok'
        tank_shop = Shop()
        return tank_shop, player

    @pytest.mark.parametrize("tankID,credits,gold, exp_credits, exp_gold",
                             [(1101, 600, 100, 100, 100), (2101, 950, 20, 100, 10), (3101, 1600, 60, 100, 10),
                              # gold and credits > price
                              (1101, 500, 0, 0, 0), (2101, 850, 10, 0, 0),
                              (3101, 1500, 50, 0, 0)])  # gold and credits = price
    def test_buyTank(self, resource_setup, tankID, credits, gold, exp_credits, exp_gold):
        errors = []
        tank_shop = resource_setup[0]
        player = resource_setup[1]
        player.inventoryPlanes = []
        player.resources.credits = credits
        player.resources.gold = gold
        tank_shop._Shop__buyTank(player, tankID)

        if not player.resources.gold == exp_gold:
            errors.append("Player gold is %s ,expected %s" % (player.resources.gold, exp_gold))
        if not player.resources.credits == exp_credits:
            errors.append("Player credits are %s ,expected %s" % (player.resources.credits, exp_credits))
        if not player.inventoryPlanes == [tankID]:
            errors.append("Player tanks: " + ",".join(map(str, player.inventoryPlanes)) +
                          " .Expected only %s in lisl" % tankID)

        assert not errors, "errors occured:\n{}".format("\n".join(errors))

    @pytest.mark.parametrize("tankID_1,tankID_2,credits,gold, exp_credits, exp_gold",
                             [(1101, 2101, 1550, 100, 200, 90), (2101, 3101, 2550, 80, 200, 20),
                              # gold and credits > price
                              (1101, 2101, 1350, 10, 0, 0),
                              (3101, 2101, 2350, 60, 0, 0)])  # gold and credits = price
    def test_buyTank_several_tanks(self, resource_setup, tankID_1, tankID_2, credits, gold, exp_credits, exp_gold):
        errors = []
        tank_shop = resource_setup[0]
        player = resource_setup[1]
        player.inventoryPlanes = []
        player.resources.credits = credits
        player.resources.gold = gold
        tank_shop._Shop__buyTank(player, tankID_1)
        tank_shop._Shop__buyTank(player, tankID_2)

        if not player.resources.gold == exp_gold:
            errors.append("Player gold is %s ,expected %s" % (player.resources.gold, exp_gold))
        if not player.resources.credits == exp_credits:
            errors.append("Player credits are %s ,expected %s" % (player.resources.credits, exp_credits))
        if not player.inventoryPlanes == [tankID_1, tankID_2]:
            errors.append("Player tanks: " + ",".join(map(str, player.inventoryPlanes)) +
                          " .Expected %s, %s in lisl" % tankID_1, tankID_2)

        assert not errors, "errors occured:\n{}".format("\n".join(errors))

    @pytest.mark.parametrize("tankID,credits,gold, exp_credits, exp_gold",
                             [(1101, 499, 0, 499, 0), (2101, 849, 9, 849, 9), (3101, 1499, 49, 1499, 49),
                              # gold <price, credits < price
                              (1101, 499, 0, 499, 0), (2101, 849, 20, 849, 20), (3101, 1499, 60, 1499, 60),
                              # gold> price, credits < price
                              (2101, 850, 9, 850, 9),
                              (3101, 1500, 49, 1500, 49)])  # credits < price, gold <price
    def test_buyTank_negative(self, resource_setup, tankID, credits, gold, exp_credits, exp_gold):
        errors = []
        tank_shop = resource_setup[0]
        player = resource_setup[1]
        player.inventoryPlanes = []
        player.resources.credits = credits
        player.resources.gold = gold
        tank_shop._Shop__buyTank(player, tankID)

        if not player.resources.gold == exp_gold:
            errors.append("Player gold is %s ,expected %s" % (player.resources.gold, exp_gold))
        if not player.resources.credits == exp_credits:
            errors.append("Player credits are %s ,expected %s" % (player.resources.credits, exp_credits))
        if not player.inventoryPlanes == []:
            errors.append("Player tanks: " + ",".join(map(str, player.inventoryPlanes)) +
                          " .Expected empty array")

        assert not errors, "errors occured:\n{}".format("\n".join(errors))

    @pytest.mark.parametrize("tankID,gunID, credits,gold, exp_credits, exp_gold",
                             [(1101, 223, 30, 10, 10, 10), (1101, 224, 10, 40, 10, 10), (2101, 555, 260, 10, 10, 10),
                              (2101, 655, 250, 10, 10, 10), (3101, 485, 230, 10, 10, 10), (3101, 286, 130, 10, 10, 10),
                              # gold > price, credits > price
                              (1101, 223, 20, 0, 0, 0), (1101, 224, 0, 30, 0, 0), (2101, 555, 250, 0, 0, 0),
                              (2101, 655, 240, 0, 0, 0), (3101, 485, 220, 0, 0, 0), (3101, 286, 120, 0, 0, 0)
                              # gold = price, credits = price
                              ])
    def test_buyGuns(self, resource_setup, tankID, gunID, credits, gold, exp_credits, exp_gold):
        errors = []
        tank_shop = resource_setup[0]
        player = resource_setup[1]
        player.inventoryPlanes = [tankID]
        player.inventoryGuns = {tankID: []}
        player.resources.credits = credits
        player.resources.gold = gold
        tank_shop._Shop__buyGuns(player, tankID, gunID)

        if not player.resources.gold == exp_gold:
            errors.append("Player gold is %s ,expected %s" % (player.resources.gold, exp_gold))
        if not player.resources.credits == exp_credits:
            errors.append("Player credits are %s ,expected %s" % (player.resources.credits, exp_credits))
        if not player.inventoryPlanes == [tankID]:
            errors.append("Player tanks: " + ",".join(map(str, player.inventoryPlanes)) +
                          " Expected only %s in list" % tankID)
        if not player.inventoryGuns[tankID] == [gunID]:
            errors.append("Player guns for given tank: " + ",".join(map(str, player.inventoryGuns[tankID])) +
                          " .Expected only %s in list" % gunID)

        assert not errors, "errors occured:\n{}".format("\n".join(errors))

    @pytest.mark.parametrize("tankID,gunID_1,gunID_2, credits,gold, exp_credits, exp_gold",
                             [(1101, 223, 224, 30, 40, 10, 10), (2101, 555, 655, 500, 10, 10, 10),
                              # gold > price, credits > price
                              (1101, 223, 224, 20, 30, 0, 0), (2101, 555, 655, 490, 0, 0, 0)
                              # gold = price, credits = price
                              ])
    def test_buyGuns_several(self, resource_setup, tankID, gunID_1, gunID_2, credits, gold, exp_credits, exp_gold):
        errors = []
        tank_shop = resource_setup[0]
        player = resource_setup[1]
        player.inventoryPlanes = [tankID]
        player.inventoryGuns = {tankID: []}
        player.resources.credits = credits
        player.resources.gold = gold
        tank_shop._Shop__buyGuns(player, tankID, gunID_1)
        tank_shop._Shop__buyGuns(player, tankID, gunID_2)

        if not player.resources.gold == exp_gold:
            errors.append("Player gold is %s ,expected %s" % (player.resources.gold, exp_gold))
        if not player.resources.credits == exp_credits:
            errors.append("Player credits are %s ,expected %s" % (player.resources.credits, exp_credits))
        if not player.inventoryPlanes == [tankID]:
            errors.append("Player tanks: " + ",".join(map(str, player.inventoryPlanes)) +
                          " Expected only %s in list" % tankID)
        if not player.inventoryGuns[tankID] == [gunID_1, gunID_2]:
            errors.append("Player guns for given tank: " + ",".join(map(str, player.inventoryGuns[tankID])) +
                          " .Expected only %s, %s in list" % gunID_1, gunID_2)

        assert not errors, "errors occured:\n{}".format("\n".join(errors))

    @pytest.mark.parametrize("tankID,gunID, credits,gold, exp_credits, exp_gold",
                             [(1101, 224, 10, 29, 10, 29),
                              # gold < price, credits = price
                              (1101, 223, 19, 0, 19, 0), (2101, 555, 249, 0, 249, 0),
                              (2101, 655, 239, 0, 239, 0), (3101, 485, 219, 0, 219, 0), (3101, 286, 119, 0, 119, 0),
                              # gold = price, credits < price
                              (3101, 286, 219, 0, 219, 0), (3101, 485, 119, 0, 119, 0)
                              # wrong gunID for given tankID
                              ])
    def test_buyGuns_negative(self, resource_setup, tankID, gunID, credits, gold, exp_credits, exp_gold):
        errors = []
        tank_shop = resource_setup[0]
        player = resource_setup[1]
        player.inventoryPlanes = [tankID]
        player.inventoryGuns = {tankID: []}
        player.resources.credits = credits
        player.resources.gold = gold
        tank_shop._Shop__buyGuns(player, tankID, gunID)

        if not player.resources.gold == exp_gold:
            errors.append("Player gold is %s ,expected %s" % (player.resources.gold, exp_gold))
        if not player.resources.credits == exp_credits:
            errors.append("Player credits are %s ,expected %s" % (player.resources.credits, exp_credits))
        if not player.inventoryPlanes == [tankID]:
            errors.append("Player tanks: " + ",".join(map(str, player.inventoryPlanes)) +
                          " Expected only %s in list" % tankID)
        if not player.inventoryGuns[tankID] == []:
            errors.append("Player guns for given tank: " + ",".join(map(str, player.inventoryGuns[tankID])) +
                          " .Expected empty array")

        assert not errors, "errors occured:\n{}".format("\n".join(errors))
