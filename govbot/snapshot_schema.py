import sgqlc.types


snapshot_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
class Any(sgqlc.types.Scalar):
    __schema__ = snapshot_schema


Boolean = sgqlc.types.Boolean

Float = sgqlc.types.Float

Int = sgqlc.types.Int

class OrderDirection(sgqlc.types.Enum):
    __schema__ = snapshot_schema
    __choices__ = ('asc', 'desc')


String = sgqlc.types.String


########################################################################
# Input Objects
########################################################################
class AliasWhere(sgqlc.types.Input):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'id_in', 'ipfs', 'ipfs_in', 'address', 'address_in', 'alias', 'alias_in', 'created', 'created_in', 'created_gt', 'created_gte', 'created_lt', 'created_lte')
    id = sgqlc.types.Field(String, graphql_name='id')
    id_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='id_in')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    ipfs_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='ipfs_in')
    address = sgqlc.types.Field(String, graphql_name='address')
    address_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='address_in')
    alias = sgqlc.types.Field(String, graphql_name='alias')
    alias_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='alias_in')
    created = sgqlc.types.Field(Int, graphql_name='created')
    created_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='created_in')
    created_gt = sgqlc.types.Field(Int, graphql_name='created_gt')
    created_gte = sgqlc.types.Field(Int, graphql_name='created_gte')
    created_lt = sgqlc.types.Field(Int, graphql_name='created_lt')
    created_lte = sgqlc.types.Field(Int, graphql_name='created_lte')


class FollowWhere(sgqlc.types.Input):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'id_in', 'ipfs', 'ipfs_in', 'follower', 'follower_in', 'space', 'space_in', 'created', 'created_in', 'created_gt', 'created_gte', 'created_lt', 'created_lte')
    id = sgqlc.types.Field(String, graphql_name='id')
    id_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='id_in')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    ipfs_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='ipfs_in')
    follower = sgqlc.types.Field(String, graphql_name='follower')
    follower_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='follower_in')
    space = sgqlc.types.Field(String, graphql_name='space')
    space_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='space_in')
    created = sgqlc.types.Field(Int, graphql_name='created')
    created_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='created_in')
    created_gt = sgqlc.types.Field(Int, graphql_name='created_gt')
    created_gte = sgqlc.types.Field(Int, graphql_name='created_gte')
    created_lt = sgqlc.types.Field(Int, graphql_name='created_lt')
    created_lte = sgqlc.types.Field(Int, graphql_name='created_lte')


class MessageWhere(sgqlc.types.Input):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'id_in', 'mci', 'mci_in', 'mci_gt', 'mci_gte', 'mci_lt', 'mci_lte', 'timestamp', 'timestamp_in', 'timestamp_gt', 'timestamp_gte', 'timestamp_lt', 'timestamp_lte', 'space', 'space_in', 'type', 'type_in')
    id = sgqlc.types.Field(String, graphql_name='id')
    id_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='id_in')
    mci = sgqlc.types.Field(Int, graphql_name='mci')
    mci_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='mci_in')
    mci_gt = sgqlc.types.Field(Int, graphql_name='mci_gt')
    mci_gte = sgqlc.types.Field(Int, graphql_name='mci_gte')
    mci_lt = sgqlc.types.Field(Int, graphql_name='mci_lt')
    mci_lte = sgqlc.types.Field(Int, graphql_name='mci_lte')
    timestamp = sgqlc.types.Field(Int, graphql_name='timestamp')
    timestamp_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='timestamp_in')
    timestamp_gt = sgqlc.types.Field(Int, graphql_name='timestamp_gt')
    timestamp_gte = sgqlc.types.Field(Int, graphql_name='timestamp_gte')
    timestamp_lt = sgqlc.types.Field(Int, graphql_name='timestamp_lt')
    timestamp_lte = sgqlc.types.Field(Int, graphql_name='timestamp_lte')
    space = sgqlc.types.Field(String, graphql_name='space')
    space_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='space_in')
    type = sgqlc.types.Field(String, graphql_name='type')
    type_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='type_in')


class ProposalWhere(sgqlc.types.Input):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'id_in', 'ipfs', 'ipfs_in', 'space', 'space_in', 'author', 'author_in', 'network', 'network_in', 'title_contains', 'strategies_contains', 'validation', 'type', 'type_in', 'created', 'created_in', 'created_gt', 'created_gte', 'created_lt', 'created_lte', 'start', 'start_in', 'start_gt', 'start_gte', 'start_lt', 'start_lte', 'end', 'end_in', 'end_gt', 'end_gte', 'end_lt', 'end_lte', 'scores_state', 'scores_state_in', 'state')
    id = sgqlc.types.Field(String, graphql_name='id')
    id_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='id_in')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    ipfs_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='ipfs_in')
    space = sgqlc.types.Field(String, graphql_name='space')
    space_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='space_in')
    author = sgqlc.types.Field(String, graphql_name='author')
    author_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='author_in')
    network = sgqlc.types.Field(String, graphql_name='network')
    network_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='network_in')
    title_contains = sgqlc.types.Field(String, graphql_name='title_contains')
    strategies_contains = sgqlc.types.Field(String, graphql_name='strategies_contains')
    validation = sgqlc.types.Field(String, graphql_name='validation')
    type = sgqlc.types.Field(String, graphql_name='type')
    type_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='type_in')
    created = sgqlc.types.Field(Int, graphql_name='created')
    created_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='created_in')
    created_gt = sgqlc.types.Field(Int, graphql_name='created_gt')
    created_gte = sgqlc.types.Field(Int, graphql_name='created_gte')
    created_lt = sgqlc.types.Field(Int, graphql_name='created_lt')
    created_lte = sgqlc.types.Field(Int, graphql_name='created_lte')
    start = sgqlc.types.Field(Int, graphql_name='start')
    start_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='start_in')
    start_gt = sgqlc.types.Field(Int, graphql_name='start_gt')
    start_gte = sgqlc.types.Field(Int, graphql_name='start_gte')
    start_lt = sgqlc.types.Field(Int, graphql_name='start_lt')
    start_lte = sgqlc.types.Field(Int, graphql_name='start_lte')
    end = sgqlc.types.Field(Int, graphql_name='end')
    end_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='end_in')
    end_gt = sgqlc.types.Field(Int, graphql_name='end_gt')
    end_gte = sgqlc.types.Field(Int, graphql_name='end_gte')
    end_lt = sgqlc.types.Field(Int, graphql_name='end_lt')
    end_lte = sgqlc.types.Field(Int, graphql_name='end_lte')
    scores_state = sgqlc.types.Field(String, graphql_name='scores_state')
    scores_state_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='scores_state_in')
    state = sgqlc.types.Field(String, graphql_name='state')


class SpaceWhere(sgqlc.types.Input):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'id_in')
    id = sgqlc.types.Field(String, graphql_name='id')
    id_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='id_in')


class SubscriptionWhere(sgqlc.types.Input):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'id_in', 'ipfs', 'ipfs_in', 'address', 'address_in', 'space', 'space_in', 'created', 'created_in', 'created_gt', 'created_gte', 'created_lt', 'created_lte')
    id = sgqlc.types.Field(String, graphql_name='id')
    id_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='id_in')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    ipfs_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='ipfs_in')
    address = sgqlc.types.Field(String, graphql_name='address')
    address_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='address_in')
    space = sgqlc.types.Field(String, graphql_name='space')
    space_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='space_in')
    created = sgqlc.types.Field(Int, graphql_name='created')
    created_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='created_in')
    created_gt = sgqlc.types.Field(Int, graphql_name='created_gt')
    created_gte = sgqlc.types.Field(Int, graphql_name='created_gte')
    created_lt = sgqlc.types.Field(Int, graphql_name='created_lt')
    created_lte = sgqlc.types.Field(Int, graphql_name='created_lte')


class UsersWhere(sgqlc.types.Input):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'id_in', 'ipfs', 'ipfs_in', 'created', 'created_in', 'created_gt', 'created_gte', 'created_lt', 'created_lte')
    id = sgqlc.types.Field(String, graphql_name='id')
    id_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='id_in')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    ipfs_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='ipfs_in')
    created = sgqlc.types.Field(Int, graphql_name='created')
    created_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='created_in')
    created_gt = sgqlc.types.Field(Int, graphql_name='created_gt')
    created_gte = sgqlc.types.Field(Int, graphql_name='created_gte')
    created_lt = sgqlc.types.Field(Int, graphql_name='created_lt')
    created_lte = sgqlc.types.Field(Int, graphql_name='created_lte')


class VoteWhere(sgqlc.types.Input):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'id_in', 'ipfs', 'ipfs_in', 'space', 'space_in', 'voter', 'voter_in', 'proposal', 'proposal_in', 'created', 'created_in', 'created_gt', 'created_gte', 'created_lt', 'created_lte', 'vp', 'vp_in', 'vp_gt', 'vp_gte', 'vp_lt', 'vp_lte', 'vp_state', 'vp_state_in')
    id = sgqlc.types.Field(String, graphql_name='id')
    id_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='id_in')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    ipfs_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='ipfs_in')
    space = sgqlc.types.Field(String, graphql_name='space')
    space_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='space_in')
    voter = sgqlc.types.Field(String, graphql_name='voter')
    voter_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='voter_in')
    proposal = sgqlc.types.Field(String, graphql_name='proposal')
    proposal_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='proposal_in')
    created = sgqlc.types.Field(Int, graphql_name='created')
    created_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='created_in')
    created_gt = sgqlc.types.Field(Int, graphql_name='created_gt')
    created_gte = sgqlc.types.Field(Int, graphql_name='created_gte')
    created_lt = sgqlc.types.Field(Int, graphql_name='created_lt')
    created_lte = sgqlc.types.Field(Int, graphql_name='created_lte')
    vp = sgqlc.types.Field(Float, graphql_name='vp')
    vp_in = sgqlc.types.Field(sgqlc.types.list_of(Float), graphql_name='vp_in')
    vp_gt = sgqlc.types.Field(Float, graphql_name='vp_gt')
    vp_gte = sgqlc.types.Field(Float, graphql_name='vp_gte')
    vp_lt = sgqlc.types.Field(Float, graphql_name='vp_lt')
    vp_lte = sgqlc.types.Field(Float, graphql_name='vp_lte')
    vp_state = sgqlc.types.Field(String, graphql_name='vp_state')
    vp_state_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='vp_state_in')



########################################################################
# Output Objects and Interfaces
########################################################################
class Alias(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'ipfs', 'address', 'alias', 'created')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    address = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='address')
    alias = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='alias')
    created = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='created')


class Follow(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'ipfs', 'follower', 'space', 'created')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    follower = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='follower')
    space = sgqlc.types.Field(sgqlc.types.non_null('Space'), graphql_name='space')
    created = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='created')


class Item(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'spaces_count')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    spaces_count = sgqlc.types.Field(Int, graphql_name='spacesCount')


class Message(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('mci', 'id', 'ipfs', 'address', 'version', 'timestamp', 'space', 'type', 'sig', 'receipt')
    mci = sgqlc.types.Field(Int, graphql_name='mci')
    id = sgqlc.types.Field(String, graphql_name='id')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    address = sgqlc.types.Field(String, graphql_name='address')
    version = sgqlc.types.Field(String, graphql_name='version')
    timestamp = sgqlc.types.Field(Int, graphql_name='timestamp')
    space = sgqlc.types.Field(String, graphql_name='space')
    type = sgqlc.types.Field(String, graphql_name='type')
    sig = sgqlc.types.Field(String, graphql_name='sig')
    receipt = sgqlc.types.Field(String, graphql_name='receipt')


class Proposal(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'ipfs', 'author', 'created', 'space', 'network', 'symbol', 'type', 'strategies', 'validation', 'plugins', 'title', 'body', 'discussion', 'choices', 'start', 'end', 'quorum', 'privacy', 'snapshot', 'state', 'link', 'app', 'scores', 'scores_by_strategy', 'scores_state', 'scores_total', 'scores_updated', 'votes')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    author = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='author')
    created = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='created')
    space = sgqlc.types.Field('Space', graphql_name='space')
    network = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='network')
    symbol = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='symbol')
    type = sgqlc.types.Field(String, graphql_name='type')
    strategies = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Strategy')), graphql_name='strategies')
    validation = sgqlc.types.Field('Validation', graphql_name='validation')
    plugins = sgqlc.types.Field(sgqlc.types.non_null(Any), graphql_name='plugins')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    body = sgqlc.types.Field(String, graphql_name='body')
    discussion = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='discussion')
    choices = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='choices')
    start = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='start')
    end = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='end')
    quorum = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='quorum')
    privacy = sgqlc.types.Field(String, graphql_name='privacy')
    snapshot = sgqlc.types.Field(String, graphql_name='snapshot')
    state = sgqlc.types.Field(String, graphql_name='state')
    link = sgqlc.types.Field(String, graphql_name='link')
    app = sgqlc.types.Field(String, graphql_name='app')
    scores = sgqlc.types.Field(sgqlc.types.list_of(Float), graphql_name='scores')
    scores_by_strategy = sgqlc.types.Field(Any, graphql_name='scores_by_strategy')
    scores_state = sgqlc.types.Field(String, graphql_name='scores_state')
    scores_total = sgqlc.types.Field(Float, graphql_name='scores_total')
    scores_updated = sgqlc.types.Field(Int, graphql_name='scores_updated')
    votes = sgqlc.types.Field(Int, graphql_name='votes')


class Query(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('space', 'spaces', 'proposal', 'proposals', 'vote', 'votes', 'aliases', 'follows', 'subscriptions', 'users', 'user', 'skins', 'networks', 'validations', 'plugins', 'strategies', 'strategy', 'vp', 'messages')
    space = sgqlc.types.Field('Space', graphql_name='space', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(String, graphql_name='id', default=None)),
))
    )
    spaces = sgqlc.types.Field(sgqlc.types.list_of('Space'), graphql_name='spaces', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('where', sgqlc.types.Arg(SpaceWhere, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(String, graphql_name='orderBy', default=None)),
        ('order_direction', sgqlc.types.Arg(OrderDirection, graphql_name='orderDirection', default=None)),
))
    )
    proposal = sgqlc.types.Field(Proposal, graphql_name='proposal', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(String, graphql_name='id', default=None)),
))
    )
    proposals = sgqlc.types.Field(sgqlc.types.list_of(Proposal), graphql_name='proposals', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('where', sgqlc.types.Arg(ProposalWhere, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(String, graphql_name='orderBy', default=None)),
        ('order_direction', sgqlc.types.Arg(OrderDirection, graphql_name='orderDirection', default=None)),
))
    )
    vote = sgqlc.types.Field('Vote', graphql_name='vote', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(String, graphql_name='id', default=None)),
))
    )
    votes = sgqlc.types.Field(sgqlc.types.list_of('Vote'), graphql_name='votes', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('where', sgqlc.types.Arg(VoteWhere, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(String, graphql_name='orderBy', default=None)),
        ('order_direction', sgqlc.types.Arg(OrderDirection, graphql_name='orderDirection', default=None)),
))
    )
    aliases = sgqlc.types.Field(sgqlc.types.list_of(Alias), graphql_name='aliases', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('where', sgqlc.types.Arg(AliasWhere, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(String, graphql_name='orderBy', default=None)),
        ('order_direction', sgqlc.types.Arg(OrderDirection, graphql_name='orderDirection', default=None)),
))
    )
    follows = sgqlc.types.Field(sgqlc.types.list_of(Follow), graphql_name='follows', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('where', sgqlc.types.Arg(FollowWhere, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(String, graphql_name='orderBy', default=None)),
        ('order_direction', sgqlc.types.Arg(OrderDirection, graphql_name='orderDirection', default=None)),
))
    )
    subscriptions = sgqlc.types.Field(sgqlc.types.list_of('Subscription'), graphql_name='subscriptions', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('where', sgqlc.types.Arg(SubscriptionWhere, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(String, graphql_name='orderBy', default=None)),
        ('order_direction', sgqlc.types.Arg(OrderDirection, graphql_name='orderDirection', default=None)),
))
    )
    users = sgqlc.types.Field(sgqlc.types.list_of('User'), graphql_name='users', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('where', sgqlc.types.Arg(UsersWhere, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(String, graphql_name='orderBy', default=None)),
        ('order_direction', sgqlc.types.Arg(OrderDirection, graphql_name='orderDirection', default=None)),
))
    )
    user = sgqlc.types.Field('User', graphql_name='user', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(String, graphql_name='id', default=None)),
))
    )
    skins = sgqlc.types.Field(sgqlc.types.list_of(Item), graphql_name='skins')
    networks = sgqlc.types.Field(sgqlc.types.list_of(Item), graphql_name='networks')
    validations = sgqlc.types.Field(sgqlc.types.list_of(Item), graphql_name='validations')
    plugins = sgqlc.types.Field(sgqlc.types.list_of(Item), graphql_name='plugins')
    strategies = sgqlc.types.Field(sgqlc.types.list_of('StrategyItem'), graphql_name='strategies')
    strategy = sgqlc.types.Field('StrategyItem', graphql_name='strategy', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(String, graphql_name='id', default=None)),
))
    )
    vp = sgqlc.types.Field('Vp', graphql_name='vp', args=sgqlc.types.ArgDict((
        ('voter', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='voter', default=None)),
        ('space', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='space', default=None)),
        ('proposal', sgqlc.types.Arg(String, graphql_name='proposal', default=None)),
))
    )
    messages = sgqlc.types.Field(sgqlc.types.list_of(Message), graphql_name='messages', args=sgqlc.types.ArgDict((
        ('first', sgqlc.types.Arg(Int, graphql_name='first', default=None)),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('where', sgqlc.types.Arg(MessageWhere, graphql_name='where', default=None)),
        ('order_by', sgqlc.types.Arg(String, graphql_name='orderBy', default=None)),
        ('order_direction', sgqlc.types.Arg(OrderDirection, graphql_name='orderDirection', default=None)),
))
    )


class Space(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'name', 'private', 'about', 'avatar', 'terms', 'location', 'website', 'twitter', 'github', 'coingecko', 'email', 'network', 'symbol', 'skin', 'domain', 'strategies', 'admins', 'members', 'filters', 'plugins', 'voting', 'categories', 'validation', 'vote_validation', 'treasuries', 'followers_count', 'proposals_count', 'parent', 'children', 'guidelines', 'template')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    private = sgqlc.types.Field(Boolean, graphql_name='private')
    about = sgqlc.types.Field(String, graphql_name='about')
    avatar = sgqlc.types.Field(String, graphql_name='avatar')
    terms = sgqlc.types.Field(String, graphql_name='terms')
    location = sgqlc.types.Field(String, graphql_name='location')
    website = sgqlc.types.Field(String, graphql_name='website')
    twitter = sgqlc.types.Field(String, graphql_name='twitter')
    github = sgqlc.types.Field(String, graphql_name='github')
    coingecko = sgqlc.types.Field(String, graphql_name='coingecko')
    email = sgqlc.types.Field(String, graphql_name='email')
    network = sgqlc.types.Field(String, graphql_name='network')
    symbol = sgqlc.types.Field(String, graphql_name='symbol')
    skin = sgqlc.types.Field(String, graphql_name='skin')
    domain = sgqlc.types.Field(String, graphql_name='domain')
    strategies = sgqlc.types.Field(sgqlc.types.list_of('Strategy'), graphql_name='strategies')
    admins = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='admins')
    members = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='members')
    filters = sgqlc.types.Field('SpaceFilters', graphql_name='filters')
    plugins = sgqlc.types.Field(Any, graphql_name='plugins')
    voting = sgqlc.types.Field('SpaceVoting', graphql_name='voting')
    categories = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='categories')
    validation = sgqlc.types.Field('Validation', graphql_name='validation')
    vote_validation = sgqlc.types.Field('Validation', graphql_name='voteValidation')
    treasuries = sgqlc.types.Field(sgqlc.types.list_of('Treasury'), graphql_name='treasuries')
    followers_count = sgqlc.types.Field(Int, graphql_name='followersCount')
    proposals_count = sgqlc.types.Field(Int, graphql_name='proposalsCount')
    parent = sgqlc.types.Field('Space', graphql_name='parent')
    children = sgqlc.types.Field(sgqlc.types.list_of('Space'), graphql_name='children')
    guidelines = sgqlc.types.Field(String, graphql_name='guidelines')
    template = sgqlc.types.Field(String, graphql_name='template')


class SpaceFilters(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('min_score', 'only_members')
    min_score = sgqlc.types.Field(Float, graphql_name='minScore')
    only_members = sgqlc.types.Field(Boolean, graphql_name='onlyMembers')


class SpaceVoting(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('delay', 'period', 'type', 'quorum', 'blind', 'hide_abstain', 'privacy', 'aliased')
    delay = sgqlc.types.Field(Int, graphql_name='delay')
    period = sgqlc.types.Field(Int, graphql_name='period')
    type = sgqlc.types.Field(String, graphql_name='type')
    quorum = sgqlc.types.Field(Float, graphql_name='quorum')
    blind = sgqlc.types.Field(Boolean, graphql_name='blind')
    hide_abstain = sgqlc.types.Field(Boolean, graphql_name='hideAbstain')
    privacy = sgqlc.types.Field(String, graphql_name='privacy')
    aliased = sgqlc.types.Field(Boolean, graphql_name='aliased')


class Strategy(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('name', 'network', 'params')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    network = sgqlc.types.Field(String, graphql_name='network')
    params = sgqlc.types.Field(Any, graphql_name='params')


class StrategyItem(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'author', 'version', 'schema', 'examples', 'about', 'spaces_count')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    author = sgqlc.types.Field(String, graphql_name='author')
    version = sgqlc.types.Field(String, graphql_name='version')
    schema = sgqlc.types.Field(Any, graphql_name='schema')
    examples = sgqlc.types.Field(sgqlc.types.list_of(Any), graphql_name='examples')
    about = sgqlc.types.Field(String, graphql_name='about')
    spaces_count = sgqlc.types.Field(Int, graphql_name='spacesCount')


class Subscription(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'ipfs', 'address', 'space', 'created')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    address = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='address')
    space = sgqlc.types.Field(sgqlc.types.non_null(Space), graphql_name='space')
    created = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='created')


class Treasury(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('name', 'address', 'network')
    name = sgqlc.types.Field(String, graphql_name='name')
    address = sgqlc.types.Field(String, graphql_name='address')
    network = sgqlc.types.Field(String, graphql_name='network')


class User(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'ipfs', 'name', 'about', 'avatar', 'created')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    name = sgqlc.types.Field(String, graphql_name='name')
    about = sgqlc.types.Field(String, graphql_name='about')
    avatar = sgqlc.types.Field(String, graphql_name='avatar')
    created = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='created')


class Validation(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('name', 'params')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    params = sgqlc.types.Field(Any, graphql_name='params')


class Vote(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('id', 'ipfs', 'voter', 'created', 'space', 'proposal', 'choice', 'metadata', 'reason', 'app', 'vp', 'vp_by_strategy', 'vp_state')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    ipfs = sgqlc.types.Field(String, graphql_name='ipfs')
    voter = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='voter')
    created = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='created')
    space = sgqlc.types.Field(sgqlc.types.non_null(Space), graphql_name='space')
    proposal = sgqlc.types.Field(Proposal, graphql_name='proposal')
    choice = sgqlc.types.Field(sgqlc.types.non_null(Any), graphql_name='choice')
    metadata = sgqlc.types.Field(Any, graphql_name='metadata')
    reason = sgqlc.types.Field(String, graphql_name='reason')
    app = sgqlc.types.Field(String, graphql_name='app')
    vp = sgqlc.types.Field(Float, graphql_name='vp')
    vp_by_strategy = sgqlc.types.Field(sgqlc.types.list_of(Float), graphql_name='vp_by_strategy')
    vp_state = sgqlc.types.Field(String, graphql_name='vp_state')


class Vp(sgqlc.types.Type):
    __schema__ = snapshot_schema
    __field_names__ = ('vp', 'vp_by_strategy', 'vp_state')
    vp = sgqlc.types.Field(Float, graphql_name='vp')
    vp_by_strategy = sgqlc.types.Field(sgqlc.types.list_of(Float), graphql_name='vp_by_strategy')
    vp_state = sgqlc.types.Field(String, graphql_name='vp_state')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
snapshot_schema.query_type = Query
snapshot_schema.mutation_type = None
snapshot_schema.subscription_type = Subscription

