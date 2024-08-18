API_VERSION = 'API_v1.0'
MOD_NAME = 'BuildInfo'
LOG_NAME = 'BuildInfo, ModsAPI'

log_file = open('captainbuild.mod.log', 'w')

url = 'encoded_url'

def log(message):
    log_file.write('{} {}\n'.format(
        utils.timeNow().strftime("%Y-%m-%d %H:%M:%S"), message))
    log_file.flush()

class BuildInfo:

    def __init__(self):
        log('__init__')
        events.onBattleStart(self.battle_start)

        if not web.addAllowedUrl(url):
            log('failed to add url')

    def battle_start(self):
        log('battle_start')
        vehicle = battle.getSelfPlayerShip()

        log('{}'.format(vehicle))
        log('{}'.format(vehicle.__dict__))
        try:
            log(vehicle.id)
        except Exception as e:
            log(e)

        self.send_update(
            player=battle.getSelfPlayerInfo(),
            vehicleId=battle.getSelfPlayerInfo().shipInfo.id,
            vehicle=vehicle,
            skills=vehicle.getCommanderSkills(),
            modernizations=vehicle.getModernizations()
        )


    def _player_info_to_dict(self, player):
        return {
            'id': player.accountDBID,
            'realm': player.realm,
            'name': player.name,
        }

    def _vehicle_to_dict(self, vehicleId, vehicle):
        return {
            'id': vehicleId, # use ID that is available in the wargaming web api
            'name': vehicle.name,
            'subtype': vehicle.subtype,
        }

    def _modernizations_to_dict(self, modernizations):
        return [{
            'type': mod.type,
            'slot': mod.slotNumber,
            'icon': mod.iconPath.replace('url:../modernization_icons/icon_modernization_', ''),
        } for mod in modernizations]
    
    def _skills_to_dict(self, skills):
        return [
            [{
                'name': skill.name,
                'learned': skill.isLearned,
                'epic': skill.isEpic,
                'iconPath': skill.iconPath.replace('url:../crew_commander/skills/', ''),
            } for skill in row ] for row in skills]
        
    def send_update(self, player, vehicleId, vehicle, skills, modernizations):
        try:
            data = {
                'player': self._player_info_to_dict(player),
                'vehicle': self._vehicle_to_dict(vehicleId, vehicle),
                'modernizations': self._modernizations_to_dict(modernizations),
                'skills': self._skills_to_dict(skills),
            }
            log('sending update')
            log(data)

            res = web.openUrl('https://buildinfo.fly.dev/api/update', {
                'modernizations': self._modernizations_to_dict(modernizations),
                'skills': self._skills_to_dict(skills),
            })
            log(res)
            log(res.read())
        except Exception as e:
            log('failed send_update')
            log(e)


BuildInfo()
