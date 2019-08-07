class fin_logger():
    def log_state(self, player):
        print("\nPlayer resources: %s gold, %s credits"%(player.resources.gold, player.resources.credits))
        print("Player tanks: "+",".join(map(str, player.inventoryPlanes)))
        print("Player guns   : " + ",".join(map(str, player.inventoryGuns)))