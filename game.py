import pymunk

def logic(rocket, ground, rocket_pos, lz_offset, space):
    if lz_offset <= rocket_pos[0] <= lz_offset + 20000:
        pass

    def coll_begin(arbiter, space, data):
        print(arbiter.shapes[0].id, arbiter.shapes[1].id)
        if arbiter.shapes[0].id == 2 and  arbiter.shapes[1].id == 0:
            print('boom')

        if (arbiter.shapes[0].id == 2 or arbiter.shapes[1].id == 2) and (arbiter.shapes[0].id == 1 or arbiter.shapes[1].id == 1):
            print('landed')

        return True

    handler = space.add_default_collision_handler()

    handler.begin = coll_begin
